"""
Sistema de Validación y Modelos de KardoCore

Micro-sistema de validación propio inspirado en Pydantic pero implementado desde cero.
Aprovecha la evaluación diferida de anotaciones de Python 3.14 (PEP 649/749).
"""

import inspect
from typing import Any, Dict, get_type_hints, get_origin, get_args, Optional, Union, Callable
from datetime import datetime
# Compatibility for Python 3.11 (annotationlib is only in 3.14+)
try:
    from annotationlib import get_annotations, Format
except ImportError:
    # Fallback for Python 3.11
    def get_annotations(obj, *, eval_str=False, format=None):
        return get_type_hints(obj) if eval_str else getattr(obj, '__annotations__', {})
    Format = None


class ValidationError(Exception):
    """Excepción lanzada cuando la validación de un modelo falla."""
    
    def __init__(self, errors: Dict[str, list[str]]):
        self.errors = errors
        super().__init__(self._format_errors())
    
    def _format_errors(self) -> str:
        """Formatea los errores de validación para mostrarlos."""
        lines = ["Validation failed:"]
        for field, field_errors in self.errors.items():
            for error in field_errors:
                lines.append(f"  - {field}: {error}")
        return "\n".join(lines)


class FieldInfo:
    """Información y validadores para un campo del modelo."""
    
    def __init__(
        self,
        *,
        default: Any = None,
        required: bool = True,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        regex: Optional[str] = None,
        validator: Optional[Callable] = None,
    ):
        self.default = default
        self.required = required
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value
        self.regex = regex
        self.validator = validator
    
    def validate(self, value: Any, field_name: str) -> list[str]:
        """Valida un valor según las reglas definidas."""
        errors = []
        
        # Validación de longitud para strings y colecciones
        if self.min_length is not None and hasattr(value, '__len__'):
            if len(value) < self.min_length:
                errors.append(f"must have at least {self.min_length} characters/items")
        
        if self.max_length is not None and hasattr(value, '__len__'):
            if len(value) > self.max_length:
                errors.append(f"must have at most {self.max_length} characters/items")
        
        # Validación de rango para números
        if self.min_value is not None and isinstance(value, (int, float)):
            if value < self.min_value:
                errors.append(f"must be at least {self.min_value}")
        
        if self.max_value is not None and isinstance(value, (int, float)):
            if value > self.max_value:
                errors.append(f"must be at most {self.max_value}")
        
        # Validación con regex
        if self.regex is not None and isinstance(value, str):
            import re
            if not re.match(self.regex, value):
                errors.append(f"does not match pattern {self.regex}")
        
        # Validador personalizado
        if self.validator is not None:
            try:
                if not self.validator(value):
                    errors.append("failed custom validation")
            except Exception as e:
                errors.append(f"validation error: {str(e)}")
        
        return errors


class KardoModelMeta(type):
    """Metaclase para KardoModel que procesa anotaciones y configuración."""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # Crear la clase
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Procesar anotaciones usando evaluación diferida (Python 3.14)
        try:
            # Obtener anotaciones en formato FORWARDREF para evaluación diferida
            annotations = get_annotations(
                cls,
                format=Format.FORWARDREF,
                eval_str=False
            )
        except Exception:
            # Fallback para compatibilidad
            annotations = getattr(cls, '__annotations__', {})
        
        # Almacenar información de campos
        cls.__kardo_fields__ = {}
        
        for field_name, field_type in annotations.items():
            # Obtener FieldInfo si existe
            field_info = namespace.get(field_name)
            
            if not isinstance(field_info, FieldInfo):
                # Crear FieldInfo por defecto
                field_info = FieldInfo(required=True)
            
            cls.__kardo_fields__[field_name] = {
                'type': field_type,
                'info': field_info
            }
        
        return cls


class KardoModel(metaclass=KardoModelMeta):
    """
    Clase base para modelos de datos con validación automática.
    
    Características:
    - Validación de tipos en tiempo de ejecución
    - Conversión automática de tipos cuando es posible
    - Serialización a dict/JSON
    - Evaluación diferida de anotaciones (Python 3.14)
    
    Ejemplo:
        class User(KardoModel):
            id: int = FieldInfo(required=False)
            name: str = FieldInfo(min_length=2, max_length=100)
            email: str = FieldInfo(regex=r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$')
            created_at: datetime = FieldInfo(default=datetime.now)
    """
    
    def __init__(self, **data):
        """Inicializa el modelo con validación automática."""
        self.__dict__['_data'] = {}
        self.__dict__['_errors'] = {}
        
        # Validar y asignar valores
        for field_name, field_config in self.__kardo_fields__.items():
            field_info = field_config['info']
            field_type = field_config['type']
            
            # Obtener valor
            if field_name in data:
                value = data[field_name]
            elif field_info.default is not None:
                value = field_info.default() if callable(field_info.default) else field_info.default
            elif field_info.required:
                self._errors[field_name] = ["field is required"]
                continue
            else:
                continue
            
            # Validar tipo y convertir si es posible
            try:
                value = self._validate_and_convert_type(value, field_type, field_name)
            except Exception as e:
                self._errors[field_name] = [f"type error: {str(e)}"]
                continue
            
            # Validar con FieldInfo
            field_errors = field_info.validate(value, field_name)
            if field_errors:
                self._errors[field_name] = field_errors
                continue
            
            # Almacenar valor
            self._data[field_name] = value
        
        # Lanzar excepción si hay errores
        if self._errors:
            raise ValidationError(self._errors)
    
    def _validate_and_convert_type(self, value: Any, expected_type: Any, field_name: str) -> Any:
        """Valida y convierte el tipo de un valor."""
        # Obtener el tipo origin (para genéricos como list[str])
        origin = get_origin(expected_type)
        
        if origin is None:
            # Tipo simple
            if not isinstance(value, expected_type):
                # Intentar conversión
                try:
                    return expected_type(value)
                except Exception:
                    raise TypeError(f"cannot convert {type(value).__name__} to {expected_type.__name__}")
        else:
            # Tipo genérico (list, dict, etc.)
            if origin is list:
                if not isinstance(value, list):
                    raise TypeError(f"expected list, got {type(value).__name__}")
                # Validar elementos si hay args
                args = get_args(expected_type)
                if args:
                    return [self._validate_and_convert_type(item, args[0], f"{field_name}[]") for item in value]
            elif origin is dict:
                if not isinstance(value, dict):
                    raise TypeError(f"expected dict, got {type(value).__name__}")
        
        return value
    
    def __setattr__(self, name: str, value: Any):
        """Sobrescribe setattr para validar en asignación."""
        if name.startswith('_'):
            # Atributos internos
            super().__setattr__(name, value)
        elif name in self.__kardo_fields__:
            # Validar campo
            field_config = self.__kardo_fields__[name]
            field_type = field_config['type']
            field_info = field_config['info']
            
            # Validar tipo
            value = self._validate_and_convert_type(value, field_type, name)
            
            # Validar con FieldInfo
            errors = field_info.validate(value, name)
            if errors:
                raise ValidationError({name: errors})
            
            self._data[name] = value
        else:
            raise AttributeError(f"'{self.__class__.__name__}' has no field '{name}'")
    
    def __getattr__(self, name: str) -> Any:
        """Sobrescribe getattr para acceder a campos."""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def dict(self) -> Dict[str, Any]:
        """Convierte el modelo a diccionario."""
        return self._data.copy()
    
    def json(self) -> str:
        """Convierte el modelo a JSON."""
        import json
        
        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, KardoModel):
                return obj.dict()
            elif isinstance(obj, (list, tuple)):
                return [serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            return obj
        
        return json.dumps(serialize(self._data), indent=2)
    
    @classmethod
    def parse_obj(cls, obj: Dict[str, Any]) -> 'KardoModel':
        """Crea una instancia del modelo desde un diccionario."""
        return cls(**obj)
    
    @classmethod
    def parse_json(cls, json_str: str) -> 'KardoModel':
        """Crea una instancia del modelo desde JSON."""
        import json
        return cls.parse_obj(json.loads(json_str))
    
    def __repr__(self) -> str:
        """Representación del modelo."""
        fields = ", ".join(f"{k}={repr(v)}" for k, v in self._data.items())
        return f"{self.__class__.__name__}({fields})"


# Funciones helper para definir campos comunes
def String(*, min_length: Optional[int] = None, max_length: Optional[int] = None, regex: Optional[str] = None, **kwargs) -> FieldInfo:
    """Helper para campos de tipo string."""
    return FieldInfo(min_length=min_length, max_length=max_length, regex=regex, **kwargs)


def Integer(*, min_value: Optional[int] = None, max_value: Optional[int] = None, **kwargs) -> FieldInfo:
    """Helper para campos de tipo entero."""
    return FieldInfo(min_value=min_value, max_value=max_value, **kwargs)


def Email(**kwargs) -> FieldInfo:
    """Helper para campos de tipo email."""
    return FieldInfo(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$', **kwargs)


def DateTime(**kwargs) -> FieldInfo:
    """Helper para campos de tipo datetime."""
    return FieldInfo(**kwargs)


"""
Sistema de Configuración de KardoCore

Gestión de configuración tipada con soporte para variables de entorno,
archivos .env y validación automática.

Inspirado en Pydantic Settings pero implementado desde cero.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from kardocore.core.models.base import KardoModel, FieldInfo, String, Integer


class KardoSettings(KardoModel):
    """
    Clase base para configuración tipada de KardoCore.
    
    Características:
    - Carga automática desde variables de entorno
    - Soporte para archivos .env
    - Validación de tipos y valores
    - Valores por defecto
    - Prioridad: ENV > .env > defaults
    
    Ejemplo:
        class AppConfig(KardoSettings):
            debug: bool = FieldInfo(default=False)
            database_url: str = String(required=True)
            secret_key: str = String(min_length=32, required=True)
            port: int = Integer(default=8000, min_value=1, max_value=65535)
            
            class Config:
                env_file = ".env"
                env_prefix = "KARDO_"
        
        config = AppConfig()
        print(config.database_url)
    """
    
    class Config:
        """Configuración de la clase de settings."""
        env_file: Optional[str] = None
        env_prefix: str = ""
        case_sensitive: bool = False
    
    def __init__(self, **data):
        """Inicializa settings cargando desde múltiples fuentes."""
        # Cargar desde archivo .env si está especificado
        env_data = self._load_env_file()
        
        # Cargar desde variables de entorno del sistema
        sys_env_data = self._load_system_env()
        
        # Combinar datos con prioridad: data > sys_env > env_file > defaults
        combined_data = {**env_data, **sys_env_data, **data}
        
        # Inicializar modelo con datos combinados
        super().__init__(**combined_data)
    
    def _load_env_file(self) -> Dict[str, Any]:
        """Carga configuración desde archivo .env."""
        config = getattr(self, 'Config', None)
        if not config or not config.env_file:
            return {}
        
        env_file_path = Path(config.env_file)
        if not env_file_path.exists():
            return {}
        
        env_data = {}
        
        with open(env_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Ignorar comentarios y líneas vacías
                if not line or line.startswith('#'):
                    continue
                
                # Parsear línea KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remover comillas si existen
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Aplicar prefijo si está configurado
                    config = getattr(self, 'Config', None)
                    if config and config.env_prefix:
                        if key.startswith(config.env_prefix):
                            key = key[len(config.env_prefix):]
                    
                    # Convertir a minúsculas si no es case sensitive
                    if config and not config.case_sensitive:
                        key = key.lower()
                    
                    env_data[key] = value
        
        return env_data
    
    def _load_system_env(self) -> Dict[str, Any]:
        """Carga configuración desde variables de entorno del sistema."""
        config = getattr(self, 'Config', None)
        env_data = {}
        
        # Obtener todos los campos del modelo
        for field_name in self.__kardo_fields__.keys():
            # Construir nombre de variable de entorno
            env_var_name = field_name.upper()
            
            if config and config.env_prefix:
                env_var_name = f"{config.env_prefix}{env_var_name}"
            
            # Buscar en variables de entorno
            if env_var_name in os.environ:
                value = os.environ[env_var_name]
                
                # Convertir key a minúsculas si no es case sensitive
                key = field_name
                if config and not config.case_sensitive:
                    key = key.lower()
                
                env_data[key] = value
        
        return env_data
    
    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> 'KardoSettings':
        """
        Crea una instancia de settings desde archivo .env.
        
        Args:
            env_file: Path al archivo .env (opcional)
        
        Returns:
            Instancia de settings configurada
        """
        if env_file:
            # Temporalmente sobrescribir env_file
            original_env_file = getattr(cls.Config, 'env_file', None)
            cls.Config.env_file = env_file
            instance = cls()
            cls.Config.env_file = original_env_file
            return instance
        
        return cls()


# Configuración por defecto de KardoCore
class CoreSettings(KardoSettings):
    """
    Configuración principal de KardoCore.
    
    Define todas las configuraciones necesarias para el funcionamiento
    del framework.
    """
    
    # General
    debug: bool = FieldInfo(default=False)
    environment: str = String(default="development")
    
    # Servidor
    host: str = String(default="127.0.0.1")
    port: int = Integer(default=8000, min_value=1, max_value=65535)
    
    # Seguridad
    secret_key: str = String(min_length=32, required=True)
    allowed_hosts: list = FieldInfo(default=["*"])
    
    # Base de datos
    database_url: str = String(default="sqlite:///kardocore.db")
    
    # IA
    ai_enabled: bool = FieldInfo(default=True)
    ai_provider: str = String(default="openai")
    ai_api_key: str = String(required=False)
    ai_model: str = String(default="gpt-4")
    
    # Temas
    theme_frontend: str = String(default="default")
    theme_admin: str = String(default="default")
    
    # Caché
    cache_enabled: bool = FieldInfo(default=True)
    cache_ttl: int = Integer(default=3600, min_value=0)
    
    # Logging
    log_level: str = String(default="INFO")
    log_file: str = String(default="kardocore.log")
    
    class Config:
        env_file = ".env"
        env_prefix = "KARDO_"
        case_sensitive = False


def load_settings(env_file: Optional[str] = None) -> CoreSettings:
    """
    Carga la configuración de KardoCore.
    
    Args:
        env_file: Path al archivo .env (opcional)
    
    Returns:
        Instancia de CoreSettings configurada
    """
    return CoreSettings.from_env(env_file) if env_file else CoreSettings()


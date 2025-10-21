"""
Sistema de Eventos y Hooks de KardoCore

Sistema asíncrono de eventos que permite la comunicación desacoplada entre
componentes del framework, especialmente para la integración de IA y plugins.
"""

import asyncio
from typing import Any, Callable, Dict, List, Optional
from functools import wraps
import inspect


class EventManager:
    """
    Gestor centralizado de eventos del framework.
    
    Permite registrar listeners para eventos específicos y emitir eventos
    de forma asíncrona. Los eventos se procesan de forma segura con aislamiento
    de errores.
    """
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}
        self._event_history: List[Dict[str, Any]] = []
        self._max_history = 1000
    
    def on(self, event_name: str, handler: Callable) -> None:
        """
        Registra un listener para un evento específico.
        
        Args:
            event_name: Nombre del evento a escuchar
            handler: Función asíncrona o síncrona que maneja el evento
        """
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        
        self._listeners[event_name].append(handler)
    
    def off(self, event_name: str, handler: Optional[Callable] = None) -> None:
        """
        Desregistra un listener de un evento.
        
        Args:
            event_name: Nombre del evento
            handler: Handler específico a remover, o None para remover todos
        """
        if event_name not in self._listeners:
            return
        
        if handler is None:
            # Remover todos los listeners
            del self._listeners[event_name]
        else:
            # Remover listener específico
            self._listeners[event_name] = [
                h for h in self._listeners[event_name] if h != handler
            ]
    
    async def emit(self, event_name: str, *args, **kwargs) -> List[Any]:
        """
        Emite un evento de forma asíncrona.
        
        Todos los listeners registrados para este evento serán ejecutados.
        Los errores en listeners individuales no detienen la ejecución de otros.
        
        Args:
            event_name: Nombre del evento a emitir
            *args: Argumentos posicionales para los handlers
            **kwargs: Argumentos nombrados para los handlers
        
        Returns:
            Lista de resultados de cada handler
        """
        # Registrar evento en historial
        self._add_to_history(event_name, args, kwargs)
        
        if event_name not in self._listeners:
            return []
        
        results = []
        
        for handler in self._listeners[event_name]:
            try:
                # Ejecutar handler (síncrono o asíncrono)
                if inspect.iscoroutinefunction(handler):
                    result = await handler(*args, **kwargs)
                else:
                    result = handler(*args, **kwargs)
                
                results.append(result)
            except Exception as e:
                # Aislar errores - no detener ejecución de otros handlers
                print(f"Error in event handler for '{event_name}': {e}")
                results.append(None)
        
        return results
    
    def emit_sync(self, event_name: str, *args, **kwargs) -> List[Any]:
        """
        Emite un evento de forma síncrona (para contextos no asíncronos).
        
        Args:
            event_name: Nombre del evento a emitir
            *args: Argumentos posicionales para los handlers
            **kwargs: Argumentos nombrados para los handlers
        
        Returns:
            Lista de resultados de cada handler
        """
        # Crear un nuevo event loop si no existe
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.emit(event_name, *args, **kwargs))
    
    def _add_to_history(self, event_name: str, args: tuple, kwargs: dict) -> None:
        """Agrega un evento al historial."""
        from datetime import datetime
        
        self._event_history.append({
            'event': event_name,
            'timestamp': datetime.now(),
            'args_count': len(args),
            'kwargs_keys': list(kwargs.keys())
        })
        
        # Limitar tamaño del historial
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]
    
    def get_history(self, event_name: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de eventos.
        
        Args:
            event_name: Filtrar por nombre de evento específico (opcional)
            limit: Número máximo de eventos a retornar
        
        Returns:
            Lista de eventos del historial
        """
        history = self._event_history
        
        if event_name:
            history = [e for e in history if e['event'] == event_name]
        
        return history[-limit:]
    
    def clear_history(self) -> None:
        """Limpia el historial de eventos."""
        self._event_history = []
    
    def list_events(self) -> List[str]:
        """Retorna la lista de eventos que tienen listeners registrados."""
        return list(self._listeners.keys())
    
    def listener_count(self, event_name: str) -> int:
        """Retorna el número de listeners registrados para un evento."""
        return len(self._listeners.get(event_name, []))


# Instancia global del gestor de eventos
_event_manager = EventManager()


def event(event_name: str):
    """
    Decorador para registrar una función como listener de un evento.
    
    Uso:
        @event("on_content_created")
        async def handle_content_created(content):
            # Procesar contenido
            pass
    
    Args:
        event_name: Nombre del evento a escuchar
    """
    def decorator(func: Callable) -> Callable:
        _event_manager.on(event_name, func)
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# Funciones de conveniencia para acceder al gestor global
def on(event_name: str, handler: Callable) -> None:
    """Registra un listener para un evento."""
    _event_manager.on(event_name, handler)


def off(event_name: str, handler: Optional[Callable] = None) -> None:
    """Desregistra un listener de un evento."""
    _event_manager.off(event_name, handler)


async def emit(event_name: str, *args, **kwargs) -> List[Any]:
    """Emite un evento de forma asíncrona."""
    return await _event_manager.emit(event_name, *args, **kwargs)


def emit_sync(event_name: str, *args, **kwargs) -> List[Any]:
    """Emite un evento de forma síncrona."""
    return _event_manager.emit_sync(event_name, *args, **kwargs)


def get_event_manager() -> EventManager:
    """Obtiene la instancia global del gestor de eventos."""
    return _event_manager


# Eventos predefinidos del sistema
class Events:
    """Constantes para eventos predefinidos del sistema."""
    
    # Eventos del ciclo de vida
    ON_STARTUP = "on_startup"
    ON_SHUTDOWN = "on_shutdown"
    
    # Eventos de contenido
    ON_CONTENT_CREATED = "on_content_created"
    ON_CONTENT_UPDATED = "on_content_updated"
    ON_CONTENT_DELETED = "on_content_deleted"
    ON_PUBLISH = "on_publish"
    
    # Eventos de IA
    ON_AI_REQUEST = "on_ai_request"
    ON_AI_RESPONSE = "on_ai_response"
    ON_AI_ERROR = "on_ai_error"
    
    # Eventos de usuario
    ON_USER_LOGIN = "on_user_login"
    ON_USER_LOGOUT = "on_user_logout"
    ON_USER_CREATED = "on_user_created"
    
    # Eventos de plugins
    ON_PLUGIN_LOADED = "on_plugin_loaded"
    ON_PLUGIN_UNLOADED = "on_plugin_unloaded"


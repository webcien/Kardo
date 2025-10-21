"""
Módulo core de KardoCore.

Contiene los componentes fundamentales del framework:
- Aplicación ASGI
- Sistema de modelos y validación
- Sistema de eventos
- Configuración
"""

from kardocore.core.app import KardoApp, Request, Response, JSONResponse, HTMLResponse
from kardocore.core.models import KardoModel, FieldInfo, ValidationError
from kardocore.core.events import EventManager, event, Events
from kardocore.core.config import KardoSettings, CoreSettings, load_settings

__all__ = [
    "KardoApp",
    "Request",
    "Response",
    "JSONResponse",
    "HTMLResponse",
    "KardoModel",
    "FieldInfo",
    "ValidationError",
    "EventManager",
    "event",
    "Events",
    "KardoSettings",
    "CoreSettings",
    "load_settings",
]


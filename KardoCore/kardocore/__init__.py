"""
KardoCore - Framework Python Híbrido, Modular e IA-Ready

Un framework open source para crear Headless CMS, CMS completos, APIs y aplicaciones
empresariales con integración nativa de IA generativa.

Versión: 0.1.0-alpha
Licencia: MIT
Autor: Juan Quezada
Compatibilidad: Python 3.14+
"""

__version__ = "0.1.0-alpha"
__author__ = "Juan Quezada"
__license__ = "MIT"
__python_requires__ = ">=3.14"

# Importaciones principales del framework
from kardocore.core.app import KardoApp
from kardocore.core.models.base import KardoModel
from kardocore.core.config import KardoSettings
from kardocore.core.events import EventManager, event

# Exportar componentes principales
__all__ = [
    "KardoApp",
    "KardoModel",
    "KardoSettings",
    "EventManager",
    "event",
    "__version__",
]


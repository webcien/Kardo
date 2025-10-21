"""
KardoCSS - Framework CSS 100% Mobile-First

Un framework CSS utility-first diseñado para KardoCore pero completamente
independiente y utilizable en cualquier proyecto web.

Versión: 0.1.0-alpha
Licencia: MIT
Autor: Juan Quezada
"""

__version__ = "0.1.0-alpha"
__author__ = "Juan Quezada"
__license__ = "MIT"

from kardocss.core.config import KardoCSSConfig
from kardocss.compiler.compiler import KardoCSSCompiler

__all__ = [
    "KardoCSSConfig",
    "KardoCSSCompiler",
    "__version__",
]


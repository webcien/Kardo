"""
KardoCore - Package Management System
Sistema de gestión de paquetes, temas y plugins
"""

from .manager import PackageManager
from .registry import PackageRegistry
from .installer import PackageInstaller
from .theme import ThemePackage

__all__ = [
    'PackageManager',
    'PackageRegistry',
    'PackageInstaller',
    'ThemePackage',
]


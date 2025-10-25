"""
KardoCore - Modern Python CMS Framework

Fast, Typed, Secure, Modular, Intelligent, Modern
"""

__version__ = "0.2.0"
__author__ = "WebCien"
__license__ = "MIT"

# Core modules
from kardocore.db import Database
from kardocore.auth import KardoAuth
from kardocore.cli import KardoCLI

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Database",
    "KardoAuth",
    "KardoCLI",
]


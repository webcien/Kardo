"""Generador de Utilidades de Dimensiones"""

from typing import List
from kardocss.core.config import KardoCSSConfig


def generate_sizing_utilities(config: KardoCSSConfig, prefix: str) -> List[str]:
    """Genera utilidades de dimensiones."""
    utilities = []
    
    utilities.append("/* Sizing Utilities */")
    
    # Width
    utilities.append(f".{prefix}w-full {{ width: 100%; }}")
    utilities.append(f".{prefix}w-screen {{ width: 100vw; }}")
    utilities.append(f".{prefix}w-auto {{ width: auto; }}")
    
    # Height
    utilities.append(f".{prefix}h-full {{ height: 100%; }}")
    utilities.append(f".{prefix}h-screen {{ height: 100vh; }}")
    utilities.append(f".{prefix}h-auto {{ height: auto; }}")
    
    # Container
    utilities.append(f".{prefix}container {{")
    utilities.append("  width: 100%;")
    utilities.append("  margin-left: auto;")
    utilities.append("  margin-right: auto;")
    utilities.append("  padding-left: 1rem;")
    utilities.append("  padding-right: 1rem;")
    utilities.append("}")
    
    utilities.append("")
    return utilities


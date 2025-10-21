"""Generador de Utilidades de Layout"""

from typing import List
from kardocss.core.config import KardoCSSConfig


def generate_layout_utilities(config: KardoCSSConfig, prefix: str) -> List[str]:
    """Genera utilidades de layout."""
    utilities = []
    
    utilities.append("/* Layout Utilities */")
    
    # Display
    displays = ["block", "inline-block", "inline", "flex", "inline-flex", "grid", "inline-grid", "hidden"]
    for display in displays:
        if display == "hidden":
            utilities.append(f".{prefix}{display} {{ display: none; }}")
        else:
            utilities.append(f".{prefix}{display} {{ display: {display}; }}")
    
    # Flexbox
    utilities.append(f".{prefix}flex-row {{ flex-direction: row; }}")
    utilities.append(f".{prefix}flex-col {{ flex-direction: column; }}")
    utilities.append(f".{prefix}flex-wrap {{ flex-wrap: wrap; }}")
    utilities.append(f".{prefix}items-center {{ align-items: center; }}")
    utilities.append(f".{prefix}justify-center {{ justify-content: center; }}")
    utilities.append(f".{prefix}justify-between {{ justify-content: space-between; }}")
    
    # Grid
    for i in range(1, 13):
        utilities.append(f".{prefix}grid-cols-{i} {{ grid-template-columns: repeat({i}, minmax(0, 1fr)); }}")
    
    utilities.append("")
    return utilities


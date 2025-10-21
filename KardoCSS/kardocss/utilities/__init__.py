"""
Módulo de utilidades de KardoCSS
"""

from kardocss.utilities.spacing import generate_spacing_utilities
from kardocss.utilities.colors import generate_color_utilities
from kardocss.utilities.typography import generate_typography_utilities
from kardocss.utilities.layout import generate_layout_utilities
from kardocss.utilities.borders import generate_border_utilities
from kardocss.utilities.sizing import generate_sizing_utilities

__all__ = [
    "generate_spacing_utilities",
    "generate_color_utilities",
    "generate_typography_utilities",
    "generate_layout_utilities",
    "generate_border_utilities",
    "generate_sizing_utilities",
]


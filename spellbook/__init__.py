"""
Spellbook - A collection of useful data science and NLP utilities.

This package provides tools for:
- Data processing and manipulation
- Text processing and NLP
- Visualization
- Machine learning utilities
- File operations and utilities
"""

# Version
__version__ = "0.1.0"

# Package information
__author__ = "Pathompong Muangthong"
__email__ = "pathompong.mua@gmail.com"
__url__ = "https://github.com/p4zaa/SpellBook"

# Import submodules to make them available as spellbook.data, spellbook.text, etc.
from . import data
from . import text
from . import viz
from . import utils
from . import ml

# Empty __all__ to prevent direct imports of functions
__all__ = []
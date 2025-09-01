"""
Spellbook - A collection of useful data science and NLP utilities.

This package provides tools for:
- Data processing and manipulation
- Text processing and NLP
- Visualization
- Machine learning utilities
- File operations and utilities

Dependencies are managed intelligently through setup.py configuration.
"""

# Version
__version__ = "0.1.0"

# Package information
__author__ = "Pathompong Muangthong"
__email__ = "pathompong.mua@gmail.com"
__url__ = "https://github.com/p4zaa/SpellBook"

class LazyModule:
    """Lazy loading module that only imports when accessed."""
    
    def __init__(self, module_name, install_hint=None):
        self._module_name = module_name
        self._install_hint = install_hint
        self._module = None
    
    def _import(self):
        if self._module is None:
            try:
                self._module = __import__(f"spellbook.{self._module_name}", fromlist=[self._module_name])
            except ImportError as e:
                if self._install_hint:
                    raise ImportError(
                        f"Module '{self._module_name}' is not available: {e}. "
                        f"Install with: {self._install_hint}"
                    ) from e
                else:
                    raise ImportError(
                        f"Module '{self._module_name}' is not available: {e}"
                    ) from e
        return self._module
    
    def __getattr__(self, name):
        module = self._import()
        return getattr(module, name)
    
    def __dir__(self):
        module = self._import()
        return dir(module)
    
    def __repr__(self):
        if self._module is None:
            return f"<LazyModule '{self._module_name}' (not yet imported)>"
        else:
            return f"<LazyModule '{self._module_name}' (imported)>"

# Create lazy modules - no actual importing happens here
data = LazyModule("data")
text = LazyModule("text", "pip install -e .[text]")
viz = LazyModule("viz", "pip install -e .[viz]")
utils = LazyModule("utils")
ml = LazyModule("ml")
network = LazyModule("network", "pip install -e .[network]")
scraper = LazyModule("scraper", "pip install -e .[scraping]")

# Define what's available at the top level
__all__ = [
    "data",
    "text", 
    "viz",
    "utils",
    "ml",
    "network",
    "scraper",
    "__version__",
    "__author__",
    "__email__",
    "__url__"
]
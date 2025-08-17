"""
Network analysis utilities for Spellbook.

This module provides functions for:
- Independent cascade model simulations
- Network diffusion analysis
- Graph-based algorithms
"""

from .cascade import independent_cascade, celf

__all__ = [
    "independent_cascade",
    "celf",
]

#!/usr/bin/env python3
"""
Command-line interface for Spellbook.

This module provides a simple CLI for accessing Spellbook functionality.
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Spellbook - Data Science and NLP Utilities",
        prog="spellbook"
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="Spellbook 0.1.0"
    )
    
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show package information"
    )
    
    parser.add_argument(
        "--modules",
        action="store_true", 
        help="List available modules"
    )
    
    args = parser.parse_args()
    
    if args.info:
        print("Spellbook - A collection of useful data science and NLP utilities")
        print("Version: 0.1.0")
        print("Author: Pathompong Muangthong")
        print("URL: https://github.com/p4zaa/SpellBook")
        return
    
    if args.modules:
        print("Available modules:")
        print("  data     - DataFrame manipulation and data processing")
        print("  text     - Text processing and NLP utilities")
        print("  viz      - Visualization utilities")
        print("  utils    - General utility functions")
        print("  ml       - Machine learning utilities")
        print("  network  - Network analysis tools")
        print("  scraper  - Web scraping and search utilities")
        return
    
    # Default behavior - show help
    parser.print_help()

if __name__ == "__main__":
    main()

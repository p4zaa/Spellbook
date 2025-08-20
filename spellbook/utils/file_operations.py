"""
File operation utilities for Spellbook.

This module provides functions for:
- File path operations
- File discovery and listing
"""

import pathlib


def get_file_paths(path: str, file_extension: str='.csv') -> list:
    """
    Returns a list of all .file_extension files in the specified folder path.
    
    Args:
        path (str): The directory path to search in.
        file_extension (str): The file extension to search for (default: '.csv').
        
    Returns:
        list: A list of file paths matching the specified file type.
    """
    folder_path = pathlib.Path(path)
    file_paths = [pathlib.Path(file_path) for file_path in folder_path.glob(f'*{file_extension}')]
    return file_paths

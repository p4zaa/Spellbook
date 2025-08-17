"""
File operation utilities for Spellbook.

This module provides functions for:
- File path operations
- File discovery and listing
"""

import pathlib


def get_file_paths(path: str, file_type: str='.csv') -> list:
    """
    Returns a list of all .file_type files in the specified folder path.
    
    Args:
        path (str): The directory path to search in.
        file_type (str): The file extension to search for (default: '.csv').
        
    Returns:
        list: A list of file paths matching the specified file type.
    """
    folder_path = pathlib.Path(path)
    file_paths = [str(file_path) for file_path in folder_path.glob(f'*{file_type}')]
    return file_paths

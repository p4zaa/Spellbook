"""
Spellbook - A collection of useful data science and NLP utilities.

This package provides tools for:
- Data processing and manipulation
- Text processing and NLP
- Visualization
- Machine learning utilities
- File operations and utilities
"""

# Core data processing functions
from .data.dataframe import (
    flatten_dataframe,
    drop_duplicates_multilabel,
    merge_one_hot_labels
)

from .data.encoding import (
    one_hot_encode_labels,
    one_hot_encode_list_column
)

from .data.splitting import (
    train_test_one_instance_handling_split,
    dataset_preprocessing_for_multilabel_classification_tasks
)

# Text processing utilities
from .text.tokenization import tokenize_text

# Visualization utilities
from .viz.wordcloud import plot_wordcloud

# File utilities
from .utils.file_operations import get_file_paths

# Version
__version__ = "0.1.0"

__all__ = [
    # Data processing
    "flatten_dataframe",
    "drop_duplicates_multilabel", 
    "merge_one_hot_labels",
    "one_hot_encode_labels",
    "one_hot_encode_list_column",
    "train_test_one_instance_handling_split",
    "dataset_preprocessing_for_multilabel_classification_tasks",
    
    # Text processing
    "tokenize_text",
    
    # Visualization
    "plot_wordcloud",
    
    # Utilities
    "get_file_paths",
]
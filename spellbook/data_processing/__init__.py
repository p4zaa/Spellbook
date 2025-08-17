"""
Data processing utilities for Spellbook.

This module provides functions for:
- DataFrame manipulation and flattening
- Label encoding and one-hot encoding
- Dataset splitting and preprocessing
- Multilabel classification utilities
"""

from .dataframe import (
    flatten_dataframe,
    drop_duplicates_multilabel,
    merge_one_hot_labels
)

from .encoding import (
    one_hot_encode_labels,
    one_hot_encode_list_column
)

from .splitting import (
    train_test_one_instance_handling_split,
    dataset_preprocessing_for_multilabel_classification_tasks
)

__all__ = [
    "flatten_dataframe",
    "drop_duplicates_multilabel",
    "merge_one_hot_labels",
    "one_hot_encode_labels", 
    "one_hot_encode_list_column",
    "train_test_one_instance_handling_split",
    "dataset_preprocessing_for_multilabel_classification_tasks",
]

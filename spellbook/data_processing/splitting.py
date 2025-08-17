"""
Dataset splitting utilities for Spellbook.

This module provides functions for:
- Train-test splitting with special handling for single-instance labels
- Multilabel classification dataset preprocessing
"""

import polars as pl
from sklearn.model_selection import train_test_split
from .dataframe import drop_duplicates_multilabel
from .encoding import one_hot_encode_list_column


def train_test_one_instance_handling_split(
    df: pl.DataFrame,
    shuffle: bool = True,
    test_size: float = 0.2,
    random_state: int = 888,
    label_columns: list = None,
    label_combination_str_column: str = 'multilabel_powerset',
    keep_label_combination: bool = False,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    """
    Split a Polars DataFrame into training and validation sets, handling cases where
    some labels have only one instance.

    Parameters:
        df (pl.DataFrame): The input DataFrame.
        shuffle (bool): Whether to shuffle the training and validation sets.
        test_size (float): Proportion of the dataset to include in the validation set.
        random_state (int): Random seed for reproducibility.
        label_columns (list): List of label columns.
        label_combination_str_column (str): The column name containing labels.

    Returns:
        tuple[pl.DataFrame, pl.DataFrame]: Training and validation Polars DataFrames.
    """
    if label_columns:
        df = df.with_columns(
            pl.concat_str(label_columns, separator='|').alias(label_combination_str_column)
        )

    # One instance handling
    one_instance_df = df\
        .group_by(label_combination_str_column)\
        .agg(pl.col(label_combination_str_column).count().alias('count'))\
        .filter(pl.col('count') == 1)\
        .join(df, on=label_combination_str_column, how='inner')\
        .drop('count')

    split_prep_df = df\
        .filter(~pl.col(label_combination_str_column)\
                .is_in(one_instance_df.get_column(label_combination_str_column)))

    labels = split_prep_df.get_column(label_combination_str_column).to_list()

    if not keep_label_combination:
        split_prep_df = split_prep_df.drop(label_combination_str_column)
        one_instance_df = one_instance_df.drop(label_combination_str_column)

    train_df, validation_df = train_test_split(split_prep_df,
                                                random_state=random_state,
                                                test_size=test_size,
                                                stratify=labels)

    # Combine train set with one instance set
    train_df = pl.concat([train_df, one_instance_df], how="diagonal")

    if shuffle:
        train_df = train_df.sample(fraction=1, shuffle=True) #shuffle rows
        validation_df = validation_df.sample(fraction=1, shuffle=True) #shuffle rows

    return train_df, validation_df


def dataset_preprocessing_for_multilabel_classification_tasks(
        df: pl.DataFrame,
        id_columns: list[str], 
        label_columns: list[str], 
        shuffle: bool = True,
        test_size: float = 0.2,
        random_state: int = 888,
) -> tuple[pl.DataFrame, pl.DataFrame]:
    """
    Preprocesses the dataset for multilabel classification tasks.

    Steps:
        1. Removes duplicate entries based on ID and label columns.
        2. Combines multilabel columns into a single column for one-hot encoding.
        3. One-hot encodes the combined labels.
        4. Splits the dataset into training and testing sets, ensuring balanced label distribution.

    Args:
        df (pl.DataFrame): The input dataset.
        id_columns (list[str]): List of column names used to identify unique entries.
        label_columns (list[str]): List of column names containing multilabels.
        shuffle (bool, optional): Whether to shuffle the dataset before splitting. Defaults to True.
        test_size (float, optional): Proportion of the dataset to allocate to the test set. Defaults to 0.2.
        random_state (int, optional): Random seed for reproducibility. Defaults to 888.

    Returns:
        tuple[pl.DataFrame, pl.DataFrame]: A tuple containing the training and testing datasets.
    """
    df = df.pipe(drop_duplicates_multilabel,
                 id_columns=id_columns,
                 label_columns=label_columns,
                 alias='_combined_labels_')
    
    df, unique_labels = one_hot_encode_list_column(
        df, 
        list_column='_combined_labels_'
    )
    
    train, test = train_test_one_instance_handling_split(
        df,
        label_columns=unique_labels,
        shuffle=shuffle,
        test_size=test_size,
        random_state=random_state,
    )

    return train, test

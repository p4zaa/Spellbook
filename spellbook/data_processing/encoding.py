"""
Label encoding utilities for Spellbook.

This module provides functions for:
- One-hot encoding of label columns
- One-hot encoding of list columns
"""

import polars as pl


def one_hot_encode_labels(
        df: pl.DataFrame, 
        label_columns: list[str]
        ) -> pl.DataFrame:
    """
    Convert label columns in a Polars DataFrame into one-hot encoded columns, setting None values to 0.
    
    Args:
        df (pl.DataFrame): The input DataFrame.
        label_columns (list[str]): The columns containing labels to be one-hot encoded.
        
    Returns:
        pl.DataFrame: A new DataFrame with one-hot encoded columns for each unique label.
    """
    # Cast label to string type
    df = df.with_columns(
        pl.col(label_columns).cast(pl.Utf8)
    )

    # Extract unique labels across the specified columns using unpivot
    unique_labels = (
        df.unpivot(on=label_columns, variable_name="variable", value_name="value")  # Unpivot into long format
        .drop_nulls("value")  # Remove rows where 'value' is null
        .select(pl.col("value").unique())  # Extract unique label values
        .to_series()
    )
    
    # Add one-hot encoded columns for each unique label
    for label in unique_labels:
        df = df.with_columns(
            pl.any_horizontal(
                [pl.col(col) == label for col in label_columns]
            ).fill_null(False).cast(pl.Int8).alias(label)
        )
    
    # Drop the original label columns
    df = df.drop(label_columns)
    
    return df, unique_labels.to_list()


def one_hot_encode_list_column(
        df: pl.DataFrame, 
        list_column: str
        ) -> pl.DataFrame:
    """
    Convert a column with list-type entries in a Polars DataFrame 
    into one-hot encoded columns for each unique element in the lists.
    
    Args:
        df (pl.DataFrame): The input DataFrame.
        list_column (str): The column containing lists of items to be one-hot encoded.
        
    Returns:
        pl.DataFrame: A new DataFrame with one-hot encoded columns for each unique item.
    """
    # Ensure the column is of list type
    df = df.with_columns(
        pl.col(list_column).cast(pl.List(pl.Utf8))
    )
    
    # Extract unique items from the lists
    unique_labels = (
        df.select(pl.col(list_column))
        .explode(list_column)  # Flatten lists into individual rows
        .drop_nulls(list_column)  # Remove null values
        .select(pl.col(list_column).unique())  # Extract unique items
        .to_series()
    )

    # Add one-hot encoded columns for each unique item
    for item in unique_labels:
        df = df.with_columns(
            pl.col(list_column)
            .list.contains(item)  # Check if the list contains the item
            .fill_null(False)  # Handle null values
            .cast(pl.Int8)  # Convert boolean to integer
            .alias(item)  # Name the column after the item
        )
    
    # Drop the original list column
    df = df.drop(list_column)
    
    return df, unique_labels.to_list()

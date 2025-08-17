"""
DataFrame manipulation utilities for Spellbook.

This module provides functions for:
- Flattening DataFrames with multiple header rows
- Handling duplicate entries with multilabel data
- Merging one-hot encoded labels
"""

import polars as pl


def flatten_dataframe(
    df: pl.DataFrame, 
    n_column_rows: int = 1, 
    merged_columns: list | str = None, 
    infer_dtypes: bool = False,
    separator: str = "_"
) -> pl.DataFrame:
    """
    Flatten a Polars DataFrame with multiple header rows into a single header row,
    replacing '__UNNAMED__n' with the nearest valid left-side column name, ensuring unique column names,
    and optionally filling null values or re-inferring data types.

    Parameters:
        df (pl.DataFrame): The input Polars DataFrame.
        n_column_rows (int): Number of rows used as column headers.
        merged_columns (list | str): Columns to forward-fill. Pass '*' to fill all columns.
        infer_dtypes (bool): Whether to re-infer data types after flattening.
        separator (str): Separator to use when concatenating column header components.

    Returns:
        pl.DataFrame: The flattened DataFrame.
    """
    # Step 1: Replace '__UNNAMED__n' with the nearest valid left-side column name
    valid_columns = []
    last_valid = None
    for col in df.columns:
        if col.startswith("__UNNAMED__"):
            valid_columns.append(last_valid if last_valid else col)
        else:
            valid_columns.append(col)
            last_valid = col

    # Step 2: Extract the rows used as column headers and include the valid column names
    header_rows = df.head(n_column_rows).to_numpy()
    column_names = valid_columns

    # Step 3: Generate new column names by concatenating valid column names and header rows
    new_column_names = [
        separator.join(
            filter(None, [column_names[col]] + 
                   [str(header_rows[row, col]) if header_rows[row, col] is not None else "" for row in range(n_column_rows)])
        )
        for col in range(len(column_names))
    ]

    # Step 4: Ensure column names are unique
    seen = {}
    unique_column_names = []
    for name in new_column_names:
        if name in seen:
            seen[name] += 1
            unique_column_names.append(f"{name}_{seen[name]}")
        else:
            seen[name] = 0
            unique_column_names.append(name)

    # Step 5: Create the flattened DataFrame by skipping the header rows
    flattened_df = df[n_column_rows:].rename({old: new for old, new in zip(df.columns, unique_column_names)})

    # Step 6: Forward-fill null values for specified columns or all columns
    if merged_columns:
        if merged_columns == '*':
            flattened_df = flattened_df.fill_null(strategy='forward')
        else:
            flattened_df = flattened_df.with_columns(
                [pl.col(col).fill_null(strategy='forward').alias(col) for col in merged_columns]
            )

    # Step 7: Re-infer data types if requested
    if infer_dtypes:
        def infer_column_dtype(series: pl.Series):
            try:
                # Attempt to cast to float, then integer
                return series.cast(pl.Float64).cast(pl.Float64, strict=False)
            except:
                try:
                    return series.cast(pl.Float64)
                except:
                    return series  # Return as-is if casting fails

        flattened_df = flattened_df.with_columns(
            [infer_column_dtype(flattened_df[col]).alias(col) for col in flattened_df.columns]
        )

    return flattened_df


def drop_duplicates_multilabel(
    df: pl.DataFrame, 
    id_columns: list[str], 
    label_columns: list[str], 
    alias: str = '_labels_',
    lazy: bool = False,
) -> pl.DataFrame:
    """
    Combines multiple label columns into a single aggregated label per unique row identifier,
    while keeping all original columns.
    
    Args:
        df: A Polars DataFrame.
        id_columns: Column names that uniquely identify each row of the DataFrame.
        label_columns: Column names containing labels to be aggregated.
        alias: The name for the combined label column.
        lazy: If True, returns a lazy Polars DataFrame.
        
    Returns:
        A Polars DataFrame with unique rows and aggregated labels.
    """
    # Columns to preserve: all original columns except the label columns
    other_cols = [col for col in df.columns if col not in label_columns + id_columns]

    # Perform aggregation
    aggregated = (
        df.lazy() if lazy else df
    ).group_by(id_columns).agg([
        pl.concat_list(pl.col(label_columns))
        .flatten()
        .unique()
        .drop_nulls()
        .alias(alias)
    ] + [
        pl.col(col).first().alias(col) for col in other_cols
    ])

    return aggregated


def merge_one_hot_labels(
    df: pl.DataFrame,
    label_cols: list[str],
    output_col: str = "labels",
    empty_list_as_null: bool = True,
) -> pl.DataFrame:
    """
    Merge one-hot encoded label columns into a single list column of active labels.
    Automatically treats missing columns as all-zero.

    Parameters
    ----------
    df : pl.DataFrame
        The input Polars DataFrame with or without all label columns present.
    label_cols : List[str]
        List of expected one-hot label column names.
    output_col : str, optional
        The name of the output list column, by default "labels".
    empty_list_as_null : bool, optional
        If True, converts empty lists in the output to nulls, by default True.

    Returns
    -------
    pl.DataFrame
        A new DataFrame with an additional column `output_col` containing lists of active label names.
    """

    # Add missing columns as 0
    existing_cols = set(df.columns)
    missing_cols = [col for col in label_cols if col not in existing_cols]
    if missing_cols:
        df = df.with_columns([pl.lit(0).alias(col) for col in missing_cols])

    # Ensure nulls are treated as 0
    df = df.with_columns([pl.col(col).fill_null(0).alias(col) for col in label_cols])

    # Build the list of label names for rows where value == 1
    df = df.with_columns([
        pl.concat_list([
            pl.when(pl.col(col) == 1).then(pl.lit(col)).otherwise(None)
            for col in label_cols
        ]).drop_nulls().alias(output_col)
    ])

    # Optionally replace empty lists with null
    if empty_list_as_null:
        df = df.with_columns([
            pl.when(pl.col(output_col).list.len() == 0)
              .then(None)
              .otherwise(pl.col(output_col))
              .alias(output_col)
        ])

    return df

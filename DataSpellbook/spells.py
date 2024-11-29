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
                return series.cast(pl.Float64).cast(pl.Int64, strict=False)
            except:
                try:
                    return series.cast(pl.Float64)
                except:
                    return series  # Return as-is if casting fails

        flattened_df = flattened_df.with_columns(
            [infer_column_dtype(flattened_df[col]).alias(col) for col in flattened_df.columns]
        )

    return flattened_df
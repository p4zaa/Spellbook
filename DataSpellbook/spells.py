import polars as pl
from sklearn.model_selection import train_test_split

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

# Optimized verion (no join operation)
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

def _drop_duplicates_multilabel_legacy(
    df: pl.DataFrame, 
    id_columns: list[str], 
    label_columns: list[str], 
    alias: str = '_labels_',
    lazy: bool = False,
) -> pl.DataFrame:
    """
    Combines multiple label columns into a single aggregated label per unique row identifier.

    Args:
        df: A Polars DataFrame.
        id_columns: Column names that uniquely identify each row of the DataFrame.
        label_columns: Column names containing labels to be aggregated.
        alias: The name for the combined label column.

    Returns:
        A Polars DataFrame with unique rows and optional label aggregation.
    """

    # Perform label aggregation
    label_aggregation = (
        df.lazy()
        .group_by(id_columns)
        .agg(
            pl.concat_list(pl.col(label_columns))
            .flatten()
            .unique()
            .drop_nulls()
            .alias(alias)
        )
    )

    # Join aggregated labels back to the original DataFrame
    result = (
        df.lazy()
        .join(label_aggregation, on=id_columns, how='left')
        .unique(subset=id_columns, keep='any')
    )

    return result if lazy else result.collect()

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
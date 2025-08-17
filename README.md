# Spellbook

A collection of useful data science and NLP utilities for efficient data processing, text analysis, and visualization.

## Features

- **Data Processing**: DataFrame manipulation, label encoding, and dataset splitting utilities
- **Text Processing**: Multi-language tokenization (Thai and English) with stopword handling
- **Visualization**: Word cloud generation with language-specific support
- **Utilities**: File operations and general helper functions
- **Machine Learning**: Utilities for ML workflows (extensible)

## Installation

```bash
pip install -e .
```

## Project Structure

```
spellbook/
├── __init__.py                 # Main package API
├── data_processing/           # DataFrame and data manipulation utilities
│   ├── __init__.py
│   ├── dataframe.py          # DataFrame flattening, deduplication, label merging
│   ├── encoding.py           # One-hot encoding utilities
│   └── splitting.py          # Train-test splitting with special handling
├── text_processing/          # Text and NLP utilities
│   ├── __init__.py
│   └── tokenization.py       # Multi-language tokenization
├── visualization/            # Visualization utilities
│   ├── __init__.py
│   ├── wordcloud.py          # Word cloud generation
│   └── fonts/               # Font assets
├── utils/                   # General utilities
│   ├── __init__.py
│   └── file_operations.py   # File handling utilities
└── ml_utils/               # Machine learning utilities (extensible)
    └── __init__.py
```

## Usage Examples

### Data Processing

```python
import polars as pl
from spellbook import flatten_dataframe, drop_duplicates_multilabel, one_hot_encode_labels

# Flatten DataFrame with multiple header rows
df = pl.read_csv("data.csv")
flattened_df = flatten_dataframe(df, n_column_rows=2, infer_dtypes=True)

# Handle multilabel data
df = drop_duplicates_multilabel(
    df, 
    id_columns=['id'], 
    label_columns=['label1', 'label2']
)

# One-hot encode labels
df_encoded, unique_labels = one_hot_encode_labels(df, ['label1', 'label2'])
```

### Text Processing

```python
from spellbook import tokenize_text

# Thai text tokenization
thai_text = "สวัสดีครับ นี่คือตัวอย่างข้อความภาษาไทย"
tokens = tokenize_text(thai_text, language='th', keep_stopwords=False)

# English text tokenization
english_text = "Hello world! This is an example text."
tokens = tokenize_text(english_text, language='en', keep_stopwords=False)
```

### Visualization

```python
from spellbook import plot_wordcloud

# Generate Thai word cloud
plot_wordcloud(
    thai_text,
    language='th',
    title="Thai Word Cloud",
    save_path="thai_wordcloud.png"
)

# Generate English word cloud
plot_wordcloud(
    english_text,
    language='en',
    title="English Word Cloud"
)
```

### Dataset Splitting

```python
from spellbook import dataset_preprocessing_for_multilabel_classification_tasks

# Preprocess and split multilabel dataset
train_df, test_df = dataset_preprocessing_for_multilabel_classification_tasks(
    df,
    id_columns=['id'],
    label_columns=['label1', 'label2'],
    test_size=0.2,
    random_state=42
)
```

### File Operations

```python
from spellbook import get_file_paths

# Get all CSV files in a directory
csv_files = get_file_paths("data/", file_type=".csv")

# Get all Excel files
excel_files = get_file_paths("data/", file_type=".xlsx")
```

## API Reference

### Data Processing

- `flatten_dataframe()`: Flatten DataFrames with multiple header rows
- `drop_duplicates_multilabel()`: Handle duplicate entries with multilabel data
- `merge_one_hot_labels()`: Merge one-hot encoded labels into lists
- `one_hot_encode_labels()`: Convert label columns to one-hot encoding
- `one_hot_encode_list_column()`: Convert list columns to one-hot encoding
- `train_test_one_instance_handling_split()`: Split datasets with single-instance handling
- `dataset_preprocessing_for_multilabel_classification_tasks()`: Complete multilabel preprocessing pipeline

### Text Processing

- `tokenize_text()`: Multi-language text tokenization with stopword handling

### Visualization

- `plot_wordcloud()`: Generate word clouds with language-specific support

### Utilities

- `get_file_paths()`: Discover files by extension in directories

## Dependencies

- polars: Fast DataFrame operations
- scikit-learn: Machine learning utilities
- matplotlib: Visualization
- wordcloud: Word cloud generation
- pythainlp: Thai language processing
- nltk: English language processing
- numpy: Numerical operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your functionality to the appropriate module
4. Update the `__init__.py` files to expose new functions
5. Add tests and documentation
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

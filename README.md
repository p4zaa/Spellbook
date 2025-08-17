# Spellbook

A collection of useful data science and NLP utilities for efficient data processing, text analysis, and visualization.

## Features

- **Data Processing**: DataFrame manipulation, label encoding, and dataset splitting utilities
- **Text Processing**: Multi-language tokenization (Thai and English) with stopword handling
- **Visualization**: Word cloud generation with language-specific support
- **Utilities**: File operations and general helper functions
- **Machine Learning**: Utilities for ML workflows (extensible)

## Installation

### Full Installation (All Features)
```bash
pip install -e .
pip install -r requirements.txt
```

### Core Installation (Data Processing Only)
```bash
pip install -e .
pip install -r requirements-core.txt
```

### Optional Dependencies
Install additional dependencies as needed:

```bash
# For text processing (Thai/English)
pip install pythainlp nltk

# For visualization
pip install matplotlib wordcloud

# For additional utilities
pip install bloxs
```

## Usage Philosophy

This package follows an **explicit import** philosophy for better code clarity and maintainability:

- **No direct access**: Functions are not available through `spellbook.function_name()`
- **Explicit imports**: Users must import from specific modules: `from spellbook.data import flatten_dataframe`
- **Clear organization**: Each module has a focused responsibility
- **Better IDE support**: Explicit imports provide better autocomplete and documentation

This approach makes it clear where each function comes from and encourages users to understand the package structure.

## Project Structure

```
spellbook/
├── __init__.py                 # Main package API
├── data/                      # DataFrame and data manipulation utilities
│   ├── __init__.py
│   ├── dataframe.py          # DataFrame flattening, deduplication, label merging
│   ├── encoding.py           # One-hot encoding utilities
│   └── splitting.py          # Train-test splitting with special handling
├── text/                     # Text and NLP utilities
│   ├── __init__.py
│   └── tokenization.py       # Multi-language tokenization
├── viz/                      # Visualization utilities
│   ├── __init__.py
│   ├── wordcloud.py          # Word cloud generation
│   └── fonts/               # Font assets
├── utils/                    # General utilities
│   ├── __init__.py
│   └── file_operations.py   # File handling utilities
└── ml/                      # Machine learning utilities (extensible)
    └── __init__.py
```

## Usage Examples

### Data Processing

```python
import polars as pl
from spellbook.data import flatten_dataframe, drop_duplicates_multilabel
from spellbook.data import one_hot_encode_labels, merge_one_hot_labels

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
from spellbook.text import tokenize_text

# Thai text tokenization
thai_text = "สวัสดีครับ นี่คือตัวอย่างข้อความภาษาไทย"
tokens = tokenize_text(thai_text, language='th', keep_stopwords=False)

# English text tokenization
english_text = "Hello world! This is an example text."
tokens = tokenize_text(english_text, language='en', keep_stopwords=False)
```

### Visualization

```python
from spellbook.viz import plot_wordcloud

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
from spellbook.data import dataset_preprocessing_for_multilabel_classification_tasks

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
from spellbook.utils import get_file_paths

# Get all CSV files in a directory
csv_files = get_file_paths("data/", file_type=".csv")

# Get all Excel files
excel_files = get_file_paths("data/", file_type=".xlsx")
```

## API Reference

### Data Processing (`spellbook.data`)

- `flatten_dataframe()`: Flatten DataFrames with multiple header rows
- `drop_duplicates_multilabel()`: Handle duplicate entries with multilabel data
- `merge_one_hot_labels()`: Merge one-hot encoded labels into lists
- `one_hot_encode_labels()`: Convert label columns to one-hot encoding
- `one_hot_encode_list_column()`: Convert list columns to one-hot encoding
- `train_test_one_instance_handling_split()`: Split datasets with single-instance handling
- `dataset_preprocessing_for_multilabel_classification_tasks()`: Complete multilabel preprocessing pipeline

### Text Processing (`spellbook.text`)

- `tokenize_text()`: Multi-language text tokenization with stopword handling

### Visualization (`spellbook.viz`)

- `plot_wordcloud()`: Generate word clouds with language-specific support

### Utilities (`spellbook.utils`)

- `get_file_paths()`: Discover files by extension in directories

### Import Examples

```python
# Data processing
from spellbook.data import flatten_dataframe, drop_duplicates_multilabel
from spellbook.data.encoding import one_hot_encode_labels
from spellbook.data.splitting import train_test_one_instance_handling_split

# Text processing
from spellbook.text import tokenize_text

# Visualization
from spellbook.viz import plot_wordcloud

# Utilities
from spellbook.utils import get_file_paths
```

## Dependencies

### Core Dependencies (Required)
- **polars**: Fast DataFrame operations
- **numpy**: Numerical operations  
- **scikit-learn**: Machine learning utilities
- **fastexcel**: Excel file processing

### Optional Dependencies
- **matplotlib**: Visualization
- **wordcloud**: Word cloud generation
- **pythainlp**: Thai language processing
- **nltk**: English language processing
- **xlsxwriter**: Excel writing
- **bloxs**: Additional utilities

> **Note**: The package uses lazy imports, so you only need to install the dependencies for the features you plan to use. If you try to use a feature without the required dependency, you'll get a helpful error message with installation instructions.

### Dependency Management

The package is designed to be lightweight and only load dependencies when needed:

- **Core functionality** (DataFrame operations, encoding, splitting) works with just the core dependencies
- **Text processing** requires `pythainlp` (Thai) and/or `nltk` (English)
- **Visualization** requires `matplotlib` and `wordcloud`
- **Excel operations** require `fastexcel` and `xlsxwriter`

This approach allows users to install only what they need, reducing package size and avoiding conflicts.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your functionality to the appropriate module
4. Update the `__init__.py` files to expose new functions
5. Add tests and documentation
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

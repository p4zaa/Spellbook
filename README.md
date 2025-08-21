# Spellbook

A collection of useful data science and NLP utilities for efficient data processing, text analysis, and visualization.

## Features

- **Data Processing**: DataFrame manipulation, label encoding, and dataset splitting utilities
- **Text Processing**: Multi-language tokenization (Thai and English) with stopword handling
- **Visualization**: Word cloud generation with language-specific support
- **Web Scraping**: Search engine crawling with CAPTCHA detection and handling
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

This package follows a **modular import** philosophy for better code clarity and maintainability:

- **Module-level access**: Functions are available through module namespaces: `spellbook.data.flatten_dataframe()`
- **Clear organization**: Each module has a focused responsibility
- **Intuitive structure**: Follows patterns like `pandas.io`, `numpy.random`, `matplotlib.pyplot`
- **Better IDE support**: Module-level imports provide excellent autocomplete and documentation

This approach makes it clear where each function comes from while maintaining a clean, intuitive API.

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
├── scraper/                  # Web scraping and search utilities
│   ├── __init__.py
│   ├── crawler.py            # General web crawling functionality
│   ├── search.py             # Search engine crawling with CAPTCHA detection
│   └── captcha_detector.py   # Reusable CAPTCHA detection for any website
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
import spellbook

# Flatten DataFrame with multiple header rows
df = pl.read_csv("data.csv")
flattened_df = spellbook.data.flatten_dataframe(df, n_column_rows=2, infer_dtypes=True)

# Handle multilabel data
df = spellbook.data.drop_duplicates_multilabel(
    df, 
    id_columns=['id'], 
    label_columns=['label1', 'label2']
)

# One-hot encode labels
df_encoded, unique_labels = spellbook.data.one_hot_encode_labels(df, ['label1', 'label2'])
```

### Text Processing

### Web Scraping

```python
import asyncio
from spellbook.scraper.search import search_google, search_duckduckgo, search_pantip

# Google search with CAPTCHA detection
async def search_example():
    # Non-headless mode: Browser window stays open for manual CAPTCHA solving
    results = await search_google("python programming", max_results=10, headless=False)
    print(f"Found {len(results)} results")
    
    # Headless mode: Requires manual input after solving CAPTCHA
    # results = await search_google("python programming", max_results=10, headless=True)
    
    # Search across multiple platforms
    from spellbook.scraper.search import search_keywords_all_platforms
    all_results = await search_keywords_all_platforms(
        ["python", "machine learning"], 
        providers=["google", "duckduckgo"],
        max_results_per_provider=5
    )
    print(f"Found {len(all_results)} total results across platforms")

# Run the async function
asyncio.run(search_example())

# Reusable CAPTCHA detection for any website
from spellbook.scraper.captcha_detector import detect_captcha, handle_captcha

# Detect CAPTCHA from URL or HTML content
is_captcha, captcha_type, details = detect_captcha(
    url="https://example.com/captcha/verify",
    html_content="<html>Please verify you are human</html>"
)

# Handle CAPTCHA with custom patterns
from spellbook.scraper.captcha_detector import CaptchaDetector
detector = CaptchaDetector()
detector.add_captcha_pattern("mywebsite.com", ["mywebsite.com/security-check"])
detector.add_captcha_indicator("my custom security message")
```

**CAPTCHA Detection**: The scraper automatically detects CAPTCHA challenges from any website and will:
- Detect CAPTCHA redirect URLs (google.com/sorry, cloudflare.com/challenge, etc.)
- Detect CAPTCHA content in HTML responses
- Print a warning message with the redirect URL
- **Non-headless mode**: Keep browser window open and automatically detect when CAPTCHA is solved
- **Headless mode**: Wait for manual input after solving CAPTCHA
- Continue automatically after CAPTCHA resolution

**Reusable CAPTCHA Detection**: The `captcha_detector` module provides reusable CAPTCHA detection that works with any website:
- Support for multiple websites (Google, Cloudflare, DuckDuckGo, etc.)
- Custom pattern and indicator support
- Easy integration with any scraper
```python
import spellbook

# Thai text tokenization
thai_text = "สวัสดีครับ นี่คือตัวอย่างข้อความภาษาไทย"
tokens = spellbook.text.tokenize_text(thai_text, language='th', keep_stopwords=False)

# English text tokenization
english_text = "Hello world! This is an example text."
tokens = spellbook.text.tokenize_text(english_text, language='en', keep_stopwords=False)
```

### Visualization

```python
import spellbook

# Generate Thai word cloud
spellbook.viz.plot_wordcloud(
    thai_text,
    language='th',
    title="Thai Word Cloud",
    save_path="thai_wordcloud.png"
)

# Generate English word cloud
spellbook.viz.plot_wordcloud(
    english_text,
    language='en',
    title="English Word Cloud"
)
```

### Dataset Splitting

```python
import spellbook

# Preprocess and split multilabel dataset
train_df, test_df = spellbook.data.dataset_preprocessing_for_multilabel_classification_tasks(
    df,
    id_columns=['id'],
    label_columns=['label1', 'label2'],
    test_size=0.2,
    random_state=42
)
```

### Web Scraping

```python
import spellbook

# Google search with multi-window pagination (default)
urls = await spellbook.scraper.search_google(
    "travel card site:pantip.com after:2024",
    max_results=30,
    max_paginate=3,
    pagination_mode="multi_window"  # Opens separate windows for each page
)

# Google search with single-window pagination (better for CAPTCHA)
urls = await spellbook.scraper.search_google(
    "travel card site:pantip.com after:2024", 
    max_results=30,
    max_paginate=3,
    pagination_mode="single_window"  # Uses JavaScript to click next page buttons
)

# DuckDuckGo search
urls = await spellbook.scraper.search_duckduckgo(
    "python tutorial",
    max_results=20
)

# Pantip search
urls = await spellbook.scraper.search_pantip(
    "travel card",
    max_results=15,
    timebias=True  # Newest first
)

# Generic search from URL
results = await spellbook.scraper.search_from_url(
    "https://www.google.com/search?q=python+tutorial",
    max_results=10,
    pagination_mode="single_window"
)
```

**Pagination Modes**:
- **`multi_window`** (default): Opens separate browser windows for each page. More reliable but may trigger more CAPTCHAs.
- **`single_window`**: Uses JavaScript to click "next page" buttons within the same browser window. Better for CAPTCHA handling as only one session is needed.

**CAPTCHA Detection**: The scraper automatically detects CAPTCHA challenges and handles them appropriately:
- Detects CAPTCHA redirect URLs and HTML content
- In non-headless mode: Keeps browser window open for manual solving
- In headless mode: Forces visible window for CAPTCHA solving
- Automatically continues after CAPTCHA resolution

### File Operations

```python
import spellbook

# Get all CSV files in a directory
csv_files = spellbook.utils.get_file_paths("data/", file_type=".csv")

# Get all Excel files
excel_files = spellbook.utils.get_file_paths("data/", file_type=".xlsx")
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

### Web Scraping (`spellbook.scraper`)

- `search_google()`: Google search with CAPTCHA detection and pagination modes
- `search_duckduckgo()`: DuckDuckGo search
- `search_pantip()`: Pantip forum search
- `search_urls()`: Generic search across multiple providers
- `search_from_url()`: Search from a specific URL with automatic config inference
- `detect_captcha()`: Reusable CAPTCHA detection for any website

### Utilities (`spellbook.utils`)

- `get_file_paths()`: Discover files by extension in directories

### Import Examples

```python
# Main import
import spellbook

# Usage examples
spellbook.data.flatten_dataframe(...)
spellbook.text.tokenize_text(...)
spellbook.viz.plot_wordcloud(...)
spellbook.utils.get_file_paths(...)

# Alternative: Import specific modules
from spellbook import data, text, viz, utils
data.flatten_dataframe(...)
text.tokenize_text(...)
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

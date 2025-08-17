# AI Assistant Guide - Spellbook Project

## Project Overview

**Spellbook** is a personal utility library created by Pathompong Muangthong to gather and organize useful data science and NLP functions for personal use. The project serves as a collection of reusable code snippets and utilities that have been developed and refined through various data science projects.

## Project Philosophy

- **Personal Utility Library**: Created for personal use, not as a public package
- **Modular Design**: Functions are organized by domain (data, text, viz, utils, ml)
- **Lazy Imports**: Dependencies are only loaded when needed to keep the package lightweight
- **Explicit Organization**: Clear module structure with focused responsibilities
- **Practical Focus**: Functions are designed to solve real-world data science problems

## Repository Structure

```
Spellbook/
├── spellbook/                    # Main package directory
│   ├── __init__.py              # Package entry point with module imports
│   ├── data/                    # Data processing utilities
│   │   ├── __init__.py
│   │   ├── dataframe.py         # DataFrame manipulation functions
│   │   ├── encoding.py          # Label encoding functions
│   │   └── splitting.py         # Dataset splitting functions
│   ├── text/                    # Text processing utilities
│   │   ├── __init__.py
│   │   └── tokenization.py      # Multi-language tokenization
│   ├── viz/                     # Visualization utilities
│   │   ├── __init__.py
│   │   ├── wordcloud.py         # Word cloud generation
│   │   └── fonts/              # Font assets for visualization
│   ├── utils/                   # General utilities
│   │   ├── __init__.py
│   │   └── file_operations.py   # File handling functions
│   └── ml/                      # Machine learning utilities (extensible)
│       └── __init__.py
│   └── network/                 # Network analysis utilities
│       ├── __init__.py
│       └── cascade.py           # Independent cascade model simulations
├── example/                     # Example data and notebooks
├── experiment_notebooks/        # Experimental Jupyter notebooks
├── requirements.txt             # All dependencies
├── requirements-core.txt        # Core dependencies only
├── setup.py                     # Package configuration
└── README.md                    # User documentation
```

## Key Modules and Functions

### Data Processing (`spellbook.data`)

**Purpose**: DataFrame manipulation, encoding, and dataset preparation for machine learning.

**Key Functions**:
- `flatten_dataframe()`: Flatten DataFrames with multiple header rows
- `drop_duplicates_multilabel()`: Handle duplicate entries with multilabel data
- `merge_one_hot_labels()`: Merge one-hot encoded labels into lists
- `one_hot_encode_labels()`: Convert label columns to one-hot encoding
- `one_hot_encode_list_column()`: Convert list columns to one-hot encoding
- `train_test_one_instance_handling_split()`: Split datasets with single-instance handling
- `dataset_preprocessing_for_multilabel_classification_tasks()`: Complete multilabel preprocessing pipeline

**Use Cases**: Data preprocessing for machine learning, handling complex DataFrame structures, multilabel classification tasks.

### Text Processing (`spellbook.text`)

**Purpose**: Multi-language text processing with focus on Thai and English.

**Key Functions**:
- `tokenize_text()`: Multi-language text tokenization with stopword handling

**Features**:
- Thai language support using PyThaiNLP
- English language support using NLTK
- Configurable stopword handling
- Multiple tokenization engines for Thai text

**Use Cases**: Text preprocessing for NLP tasks, sentiment analysis, text classification.

### Visualization (`spellbook.viz`)

**Purpose**: Data visualization with focus on text-based visualizations.

**Key Functions**:
- `plot_wordcloud()`: Generate word clouds with language-specific support

**Features**:
- Multi-language word cloud generation
- Thai font support
- Configurable appearance and saving options
- Integration with text processing functions

**Use Cases**: Text analysis visualization, presentation materials, exploratory data analysis.

### Utilities (`spellbook.utils`)

**Purpose**: General utility functions for file operations and common tasks.

**Key Functions**:
- `get_file_paths()`: Discover files by extension in directories

**Use Cases**: File management, data loading workflows, automation scripts.

### Machine Learning (`spellbook.ml`)

**Purpose**: Machine learning utilities (currently empty, designed for future expansion).

**Planned Features**: Model evaluation, feature engineering, ML pipeline utilities.

### Network Analysis (`spellbook.network`)

**Purpose**: Network analysis and diffusion modeling utilities.

**Key Functions**:
- `independent_cascade_once()`: Run Independent Cascade model simulations

**Features**:
- Information diffusion modeling
- Influence propagation analysis
- Social network analysis
- Viral marketing simulation

**Use Cases**: Social network analysis, influence modeling, information diffusion studies.

## Dependencies and Installation

### Core Dependencies (Required)
- `polars`: Fast DataFrame operations
- `numpy`: Numerical operations
- `scikit-learn`: Machine learning utilities
- `fastexcel`: Excel file processing

### Optional Dependencies
- `matplotlib`: Visualization
- `wordcloud`: Word cloud generation
- `pythainlp`: Thai language processing
- `nltk`: English language processing
- `xlsxwriter`: Excel writing
- `bloxs`: Additional utilities
- `networkx`: Network analysis

### Installation Options
```bash
# Full installation
pip install -e .
pip install -r requirements.txt

# Core installation only
pip install -e .
pip install -r requirements-core.txt
```

## Usage Patterns

### Module-Level Access (Recommended)
```python
import spellbook

# Data processing
spellbook.data.flatten_dataframe(...)
spellbook.data.drop_duplicates_multilabel(...)

# Text processing
spellbook.text.tokenize_text(...)

# Visualization
spellbook.viz.plot_wordcloud(...)

# Utilities
spellbook.utils.get_file_paths(...)
```

### Alternative Import Patterns
```python
# Import specific modules
from spellbook import data, text, viz, utils
data.flatten_dataframe(...)

# Import specific functions
from spellbook.data import flatten_dataframe
flatten_dataframe(...)
```

## Development Context

### Personal Use Focus
- Functions are designed based on real project needs
- Emphasis on practical utility over theoretical completeness
- Thai language support reflects personal language requirements
- Functions are battle-tested in actual data science projects

### Code Quality
- Functions include comprehensive docstrings
- Type hints are used where appropriate
- Error handling with helpful error messages
- Lazy imports to manage dependencies efficiently

### Extensibility
- Modular design allows easy addition of new functions
- Clear separation of concerns
- Consistent naming conventions
- Well-documented API structure

## Common Use Cases

### Data Science Workflows
1. **Data Loading and Preprocessing**: Use `spellbook.data` functions for DataFrame manipulation
2. **Text Analysis**: Use `spellbook.text` for tokenization and `spellbook.viz` for word clouds
3. **Machine Learning Preparation**: Use encoding and splitting functions for ML pipelines
4. **File Management**: Use `spellbook.utils` for automated file operations

### Multilabel Classification
The project includes specialized functions for multilabel classification tasks:
- Handling duplicate entries with multiple labels
- One-hot encoding of label columns and list columns
- Train-test splitting with special handling for single-instance labels
- Complete preprocessing pipeline for multilabel datasets

### Thai Language Processing
Special attention to Thai language support:
- Thai text tokenization with multiple engines
- Thai stopword handling
- Thai font support for visualizations
- Integration with PyThaiNLP library

## AI Assistant Guidelines

### When Helping with This Project

1. **Understand the Personal Context**: This is a personal utility library, not a commercial product
2. **Focus on Practical Solutions**: Prioritize functionality over theoretical elegance
3. **Consider Thai Language Support**: Many functions have Thai language capabilities
4. **Maintain Modular Structure**: New functions should fit into existing modules
5. **Use Lazy Imports**: Follow the pattern of importing dependencies only when needed
6. **Preserve API Consistency**: Follow existing naming conventions and patterns

### Common Tasks You Might Help With

1. **Adding New Functions**: Help implement new utilities following the existing patterns
2. **Improving Documentation**: Enhance docstrings and README content
3. **Optimizing Performance**: Suggest improvements to existing functions
4. **Adding Tests**: Create test cases for functions
5. **Dependency Management**: Help manage and organize dependencies
6. **Code Review**: Review new code for consistency and quality

### Code Style Guidelines

- Use descriptive function names
- Include comprehensive docstrings with examples
- Add type hints where helpful
- Follow the lazy import pattern for optional dependencies
- Maintain consistent error handling
- Use the module-level access pattern for new functions

## Future Development

### Planned Enhancements
- Expand `spellbook.ml` module with ML utilities
- Add more visualization functions
- Improve performance of existing functions
- Add more language support beyond Thai and English
- Create more comprehensive test suites

### Extension Points
- New data processing functions in `spellbook.data`
- Additional text processing capabilities in `spellbook.text`
- More visualization types in `spellbook.viz`
- General utilities in `spellbook.utils`
- Machine learning utilities in `spellbook.ml`

This guide should help AI assistants understand the project's purpose, structure, and development patterns to provide more effective assistance.

# Function Reference - Spellbook

This document provides detailed information about each function in the Spellbook library, organized by module. This reference is designed to help AI assistants understand the functionality and provide accurate assistance.

## Data Processing Module (`spellbook.data`)

### DataFrame Functions (`spellbook.data.dataframe`)

#### `flatten_dataframe()`
**Purpose**: Flatten DataFrames with multiple header rows into a single header row.

**Parameters**:
- `df` (pl.DataFrame): Input DataFrame
- `n_column_rows` (int): Number of rows used as column headers (default: 1)
- `merged_columns` (list | str): Columns to forward-fill, or '*' for all columns (default: None)
- `infer_dtypes` (bool): Whether to re-infer data types (default: False)
- `separator` (str): Separator for concatenating header components (default: "_")

**Returns**: pl.DataFrame - Flattened DataFrame

**Use Case**: When working with Excel files or CSV files that have multiple header rows.

**Example**:
```python
import spellbook
df = pl.read_csv("complex_data.csv")
flattened = spellbook.data.flatten_dataframe(df, n_column_rows=2, infer_dtypes=True)
```

#### `drop_duplicates_multilabel()`
**Purpose**: Combine multiple label columns into a single aggregated label per unique row identifier.

**Parameters**:
- `df` (pl.DataFrame): Input DataFrame
- `id_columns` (list[str]): Column names that uniquely identify each row
- `label_columns` (list[str]): Column names containing labels to aggregate
- `alias` (str): Name for the combined label column (default: '_labels_')
- `lazy` (bool): Return lazy DataFrame (default: False)

**Returns**: pl.DataFrame - DataFrame with unique rows and aggregated labels

**Use Case**: Multilabel classification tasks where you need to combine multiple label columns.

**Example**:
```python
result = spellbook.data.drop_duplicates_multilabel(
    df, 
    id_columns=['id'], 
    label_columns=['tag1', 'tag2', 'tag3']
)
```

#### `merge_one_hot_labels()`
**Purpose**: Merge one-hot encoded label columns into a single list column of active labels.

**Parameters**:
- `df` (pl.DataFrame): Input DataFrame
- `label_cols` (list[str]): List of expected one-hot label column names
- `output_col` (str): Name of output list column (default: "labels")
- `empty_list_as_null` (bool): Convert empty lists to null (default: True)

**Returns**: pl.DataFrame - DataFrame with additional list column

**Use Case**: Converting one-hot encoded labels back to list format for analysis.

**Example**:
```python
result = spellbook.data.merge_one_hot_labels(
    df, 
    label_cols=['cat', 'dog', 'bird'], 
    output_col='animals'
)
```

### Encoding Functions (`spellbook.data.encoding`)

#### `one_hot_encode_labels()`
**Purpose**: Convert label columns into one-hot encoded columns.

**Parameters**:
- `df` (pl.DataFrame): Input DataFrame
- `label_columns` (list[str]): Columns containing labels to encode

**Returns**: tuple[pl.DataFrame, list] - Encoded DataFrame and list of unique labels

**Use Case**: Preparing categorical data for machine learning models.

**Example**:
```python
encoded_df, unique_labels = spellbook.data.one_hot_encode_labels(
    df, 
    ['category1', 'category2']
)
```

#### `one_hot_encode_list_column()`
**Purpose**: Convert a column with list-type entries into one-hot encoded columns.

**Parameters**:
- `df` (pl.DataFrame): Input DataFrame
- `list_column` (str): Column containing lists of items

**Returns**: tuple[pl.DataFrame, list] - Encoded DataFrame and list of unique items

**Use Case**: Encoding multilabel data where each row has a list of labels.

**Example**:
```python
encoded_df, unique_items = spellbook.data.one_hot_encode_list_column(
    df, 
    'tags'
)
```

### Splitting Functions (`spellbook.data.splitting`)

#### `train_test_one_instance_handling_split()`
**Purpose**: Split DataFrame into training and validation sets with special handling for single-instance labels.

**Parameters**:
- `df` (pl.DataFrame): Input DataFrame
- `shuffle` (bool): Whether to shuffle sets (default: True)
- `test_size` (float): Proportion for validation set (default: 0.2)
- `random_state` (int): Random seed (default: 888)
- `label_columns` (list): List of label columns (default: None)
- `label_combination_str_column` (str): Column name for label combinations (default: 'multilabel_powerset')
- `keep_label_combination` (bool): Keep the combination column (default: False)

**Returns**: tuple[pl.DataFrame, pl.DataFrame] - Training and validation DataFrames

**Use Case**: Splitting multilabel datasets while ensuring all labels are represented in training.

**Example**:
```python
train_df, val_df = spellbook.data.train_test_one_instance_handling_split(
    df, 
    label_columns=['label1', 'label2'], 
    test_size=0.2
)
```

#### `dataset_preprocessing_for_multilabel_classification_tasks()`
**Purpose**: Complete preprocessing pipeline for multilabel classification tasks.

**Parameters**:
- `df` (pl.DataFrame): Input dataset
- `id_columns` (list[str]): Column names for unique entries
- `label_columns` (list[str]): Column names containing multilabels
- `shuffle` (bool): Whether to shuffle (default: True)
- `test_size` (float): Proportion for test set (default: 0.2)
- `random_state` (int): Random seed (default: 888)

**Returns**: tuple[pl.DataFrame, pl.DataFrame] - Training and testing datasets

**Use Case**: End-to-end preprocessing for multilabel classification projects.

**Example**:
```python
train, test = spellbook.data.dataset_preprocessing_for_multilabel_classification_tasks(
    df,
    id_columns=['id'],
    label_columns=['tag1', 'tag2', 'tag3']
)
```

## Text Processing Module (`spellbook.text`)

### Tokenization Functions (`spellbook.text.tokenization`)

#### `tokenize_text()`
**Purpose**: Tokenize text based on language with stopword handling.

**Parameters**:
- `text` (str): Input text to tokenize
- `language` (str): Language ('th' for Thai, 'en' for English, default: 'th')
- `keep_stopwords` (bool): Whether to keep stopwords (default: True)
- `keep_spaces` (bool): Whether to keep space characters (default: False)
- `engine` (str): Tokenizer engine for Thai ('newmm', 'longest', 'lucene', default: 'newmm')

**Returns**: list - List of tokenized words

**Dependencies**: 
- Thai: `pythainlp`
- English: `nltk`

**Use Case**: Text preprocessing for NLP tasks in Thai or English.

**Example**:
```python
# Thai text
thai_tokens = spellbook.text.tokenize_text(
    "สวัสดีครับ นี่คือตัวอย่างข้อความ", 
    language='th', 
    keep_stopwords=False
)

# English text
english_tokens = spellbook.text.tokenize_text(
    "Hello world! This is an example.", 
    language='en', 
    keep_stopwords=False
)
```

## Visualization Module (`spellbook.viz`)

### Word Cloud Functions (`spellbook.viz.wordcloud`)

#### `plot_wordcloud()`
**Purpose**: Generate word clouds with language-specific support.

**Parameters**:
- `text` (str): Input text
- `language` (str): Language ('th' for Thai, 'en' for English, default: 'th')
- `keep_stopwords` (bool): Whether to keep stopwords (default: True)
- `font_path` (str): Path to font file (default: TH Sarabun New)
- `engine` (str): Tokenizer engine for Thai (default: 'newmm')
- `figsize` (tuple): Figure size (default: (10, 6))
- `interpolation` (str): Interpolation method (default: "bilinear")
- `title` (str): Plot title (default: None)
- `width` (int): Word cloud width (default: 800)
- `height` (int): Word cloud height (default: 400)
- `save_path` (str): Path to save image (default: None)
- `transparent` (bool): Transparent background (default: True)
- `**wordcloud_kwargs`: Additional WordCloud parameters

**Returns**: WordCloud object

**Dependencies**: `matplotlib`, `wordcloud`, `pythainlp` (for Thai), `nltk` (for English)

**Use Case**: Creating word cloud visualizations for text analysis.

**Example**:
```python
spellbook.viz.plot_wordcloud(
    thai_text,
    language='th',
    title="Thai Word Cloud",
    save_path="thai_wordcloud.png"
)
```

## Network Analysis Module (`spellbook.network`)

### Cascade Functions (`spellbook.network.cascade`)

#### `independent_cascade()`
**Purpose**: Run one Independent Cascade simulation and return the number of activated nodes.

**Parameters**:
- `G`: NetworkX directed graph with edge attributes containing activation probabilities
- `seeds` (Set[Any]): Set of seed nodes to start the cascade from
- `max_steps` (int, optional): Maximum number of simulation steps. Defaults to 99999.
- `prob_attr` (str, optional): Name of edge attribute containing activation probabilities. Defaults to 'prob'.
- `default_prob` (float, optional): Default probability to use for edges without probability attribute. Defaults to 0.1.

**Returns**: Tuple[Set[Any], List[Set[Any]]] - A tuple containing:
- Set of all activated nodes at the end of simulation
- List of sets, where each set contains the cumulative activated nodes at each step

**Dependencies**: `networkx`

**Use Case**: Information diffusion modeling and influence analysis.

**Example**:
```python
import spellbook
import networkx as nx

G = nx.DiGraph()
edges = [("A", "B", 0.4), ("B", "C", 0.5), ("C", "A", 0.3)]
for u, v, p in edges:
    G.add_edge(u, v, prob=p)

active_nodes, step_activations = spellbook.network.independent_cascade(G, {"A"})

# Use custom probability attribute
G2 = nx.DiGraph()
for u, v, p in edges:
    G2.add_edge(u, v, weight=p)
active_nodes, step_activations = spellbook.network.independent_cascade(G2, {"A"}, prob_attr='weight')

# Use default probability for all edges
G3 = nx.DiGraph()
for u, v in [("A", "B"), ("B", "C"), ("C", "A")]:
    G3.add_edge(u, v)
active_nodes, step_activations = spellbook.network.independent_cascade(G3, {"A"}, default_prob=0.5)
```

#### `celf()`
**Purpose**: Cost-Effective Lazy Forward algorithm for influence maximization.

**Parameters**:
- `G`: NetworkX directed graph with edge attributes containing activation probabilities
- `k` (int): Number of seed nodes to select
- `prob_attr` (str, optional): Name of edge attribute containing activation probabilities. Defaults to 'prob'.
- `default_prob` (float, optional): Default probability to use for edges without probability attribute. Defaults to 0.1.

**Returns**: List[Any] - List of k seed nodes that maximize influence spread

**Dependencies**: `networkx`

**Use Case**: Finding the most influential nodes in a network for marketing or information campaigns.

**Example**:
```python
import spellbook
import networkx as nx

G = nx.DiGraph()
edges = [("A", "B", 0.4), ("B", "C", 0.5), ("C", "A", 0.3), ("A", "D", 0.6)]
for u, v, p in edges:
    G.add_edge(u, v, prob=p)

seeds = spellbook.network.celf(G, k=2)

# Use custom probability attribute
G2 = nx.DiGraph()
for u, v, p in edges:
    G2.add_edge(u, v, weight=p)
seeds = spellbook.network.celf(G2, k=2, prob_attr='weight')

# Use default probability for all edges
G3 = nx.DiGraph()
for u, v in [("A", "B"), ("B", "C"), ("C", "A"), ("A", "D")]:
    G3.add_edge(u, v)
seeds = spellbook.network.celf(G3, k=2, default_prob=0.5)
```

## Utilities Module (`spellbook.utils`)

### File Operation Functions (`spellbook.utils.file_operations`)

#### `get_file_paths()`
**Purpose**: Get all files of a specific type in a directory.

**Parameters**:
- `path` (str): Directory path to search
- `file_type` (str): File extension to search for (default: '.csv')

**Returns**: list - List of file paths

**Use Case**: Batch processing of files or data loading workflows.

**Example**:
```python
csv_files = spellbook.utils.get_file_paths("data/", file_type=".csv")
excel_files = spellbook.utils.get_file_paths("data/", file_type=".xlsx")
```

## Common Usage Patterns

### Data Science Workflow
```python
import spellbook
import polars as pl

# 1. Load and preprocess data
df = pl.read_csv("data.csv")
df = spellbook.data.flatten_dataframe(df, n_column_rows=2)

# 2. Handle multilabel data
df = spellbook.data.drop_duplicates_multilabel(
    df, 
    id_columns=['id'], 
    label_columns=['tag1', 'tag2']
)

# 3. Encode labels
df_encoded, unique_labels = spellbook.data.one_hot_encode_list_column(
    df, 
    '_labels_'
)

# 4. Split dataset
train, test = spellbook.data.train_test_one_instance_handling_split(
    df_encoded,
    label_columns=unique_labels
)
```

### Text Analysis Workflow
```python
import spellbook

# 1. Tokenize text
tokens = spellbook.text.tokenize_text(
    text, 
    language='th', 
    keep_stopwords=False
)

# 2. Create visualization
spellbook.viz.plot_wordcloud(
    text,
    language='th',
    title="Thai Text Analysis"
)
```

### File Processing Workflow
```python
import spellbook

# Get all CSV files
csv_files = spellbook.utils.get_file_paths("data/", file_type=".csv")

# Process each file
for file_path in csv_files:
    # Process file...
    pass
```

### Network Analysis Workflow
```python
import spellbook
import networkx as nx

# 1. Build network
G = nx.DiGraph()
edges = [("A", "B", 0.4), ("B", "C", 0.5), ("C", "A", 0.3), ("A", "D", 0.6)]
for u, v, p in edges:
    G.add_edge(u, v, prob=p)

# 2. Test influence spread
spread = spellbook.network.independent_cascade(G, {"A"})

# 3. Find most influential nodes
seeds = spellbook.network.celf(G, k=2)
```

## Error Handling

All functions include comprehensive error handling with helpful error messages:

- **ImportError**: When optional dependencies are missing, functions provide clear installation instructions
- **ValueError**: When parameters are invalid, functions explain what went wrong
- **TypeError**: When data types are incorrect, functions provide guidance

## Performance Considerations

- **Polars**: All DataFrame operations use Polars for better performance
- **Lazy Evaluation**: Some functions support lazy evaluation for large datasets
- **Memory Efficiency**: Functions are designed to be memory-efficient
- **Batch Processing**: File operations support batch processing for efficiency

This reference should help AI assistants understand the functionality and provide accurate assistance with the Spellbook library.

# Development Guidelines - Spellbook

This document provides guidelines for AI assistants to follow when helping with the Spellbook project development, maintenance, and extension.

## Project Philosophy

### Core Principles
1. **Personal Utility First**: This is a personal library, not a commercial product
2. **Practical Over Perfect**: Focus on functionality that solves real problems
3. **Modular Design**: Keep functions focused and well-organized
4. **Quality Documentation**: Comprehensive docstrings and examples
5. **Lazy Dependencies**: Only load dependencies when needed

### Code Quality Standards
- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Include comprehensive docstrings with examples
- **Error Handling**: Provide helpful error messages with clear guidance
- **Performance**: Consider performance implications, especially for large datasets
- **Consistency**: Follow existing naming conventions and patterns

## Module Organization

### Current Module Structure
```
spellbook/
├── data/           # DataFrame and data processing
├── text/           # Text processing and NLP
├── viz/            # Visualization utilities
├── utils/          # General utilities
└── ml/             # Machine learning utilities (future)
```

### Adding New Functions

#### 1. Determine the Right Module
- **Data Processing**: `spellbook.data` - DataFrame operations, encoding, splitting
- **Text Processing**: `spellbook.text` - Tokenization, text analysis, NLP
- **Visualization**: `spellbook.viz` - Charts, plots, visual outputs
- **Utilities**: `spellbook.utils` - File operations, general helpers
- **Machine Learning**: `spellbook.ml` - Model evaluation, feature engineering

#### 2. Follow Naming Conventions
- **Function Names**: Use descriptive, lowercase names with underscores
  - Good: `flatten_dataframe`, `tokenize_text`, `plot_wordcloud`
  - Avoid: `flattenDF`, `tokenizeText`, `plotWordCloud`
- **File Names**: Use descriptive names that reflect the content
  - Good: `dataframe.py`, `tokenization.py`, `wordcloud.py`
  - Avoid: `utils.py`, `helpers.py`, `misc.py`

#### 3. Function Structure
```python
def function_name(
    param1: type1,
    param2: type2 = default_value,
    param3: type3 = None
) -> return_type:
    """
    Brief description of what the function does.

    Longer description explaining the purpose, use cases, and important details.

    Parameters:
        param1 (type1): Description of parameter 1
        param2 (type2, optional): Description of parameter 2. Defaults to default_value.
        param3 (type3, optional): Description of parameter 3. Defaults to None.

    Returns:
        return_type: Description of what is returned

    Raises:
        ValueError: When and why this error occurs
        ImportError: When dependencies are missing

    Example:
        >>> import spellbook
        >>> result = spellbook.module.function_name(data, param2="value")
        >>> print(result)
        expected_output

    Use Case:
        Brief description of when to use this function.
    """
    # Implementation here
    pass
```

## Dependency Management

### Lazy Import Pattern
Always use lazy imports for optional dependencies:

```python
def function_with_optional_dependency():
    """
    Function that requires an optional dependency.
    """
    try:
        import optional_library
    except ImportError:
        raise ImportError(
            "OptionalLibrary is required for this function. "
            "Install it with: pip install optional-library"
        )
    
    # Use the imported library
    return optional_library.some_function()
```

### Dependency Categories
- **Core Dependencies**: Required for basic functionality (polars, numpy, scikit-learn)
- **Optional Dependencies**: Only needed for specific features (matplotlib, wordcloud, pythainlp)
- **Development Dependencies**: Only needed for development (pytest, black, flake8)

## Error Handling Guidelines

### Error Message Standards
- **Clear and Actionable**: Tell users exactly what went wrong and how to fix it
- **Include Installation Instructions**: For missing dependencies
- **Provide Context**: Explain why the error occurred
- **Use Consistent Format**: Follow existing error message patterns

### Example Error Handling
```python
def example_function(data, language='en'):
    if language not in ['en', 'th']:
        raise ValueError(
            f"Language '{language}' is not supported. "
            "Supported languages: 'en' (English), 'th' (Thai)"
        )
    
    if language == 'th':
        try:
            import pythainlp
        except ImportError:
            raise ImportError(
                "PyThaiNLP is required for Thai language processing. "
                "Install it with: pip install pythainlp"
            )
```

## Testing Guidelines

### Test Structure
- **Unit Tests**: Test individual functions with various inputs
- **Integration Tests**: Test how functions work together
- **Error Tests**: Test error conditions and edge cases
- **Performance Tests**: Test with large datasets when relevant

### Test Naming
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases
- Test edge cases and error conditions

### Example Test
```python
def test_flatten_dataframe_basic():
    """Test basic DataFrame flattening functionality."""
    # Test implementation
    pass

def test_flatten_dataframe_error_handling():
    """Test error handling for invalid inputs."""
    # Test error conditions
    pass
```

## Documentation Standards

### Docstring Requirements
- **Purpose**: Clear description of what the function does
- **Parameters**: All parameters with types and descriptions
- **Returns**: What the function returns and its type
- **Examples**: Working code examples
- **Use Cases**: When to use this function
- **Dependencies**: Any optional dependencies required

### README Updates
- Update usage examples when adding new functions
- Add new functions to the API reference
- Update installation instructions if new dependencies are added
- Keep the project structure diagram current

## Performance Considerations

### Large Dataset Handling
- Use Polars for DataFrame operations (faster than pandas)
- Support lazy evaluation where appropriate
- Consider memory usage for large datasets
- Provide batch processing options when relevant

### Optimization Guidelines
- Profile functions with realistic data sizes
- Use efficient algorithms and data structures
- Consider parallel processing for CPU-intensive operations
- Cache results when appropriate

## Code Review Checklist

### Before Suggesting Changes
- [ ] Does the function fit the project's purpose?
- [ ] Is it placed in the correct module?
- [ ] Does it follow naming conventions?
- [ ] Does it have comprehensive docstrings?
- [ ] Does it handle errors appropriately?
- [ ] Does it use lazy imports for optional dependencies?
- [ ] Does it include type hints?
- [ ] Does it have example usage?
- [ ] Is it performant for typical use cases?

### Code Quality Checks
- [ ] Functions are focused and do one thing well
- [ ] Error messages are helpful and actionable
- [ ] Documentation is clear and complete
- [ ] Code is readable and well-structured
- [ ] Performance is acceptable for intended use cases

## Common Patterns

### DataFrame Processing
```python
def process_dataframe(df: pl.DataFrame, **kwargs) -> pl.DataFrame:
    """
    Process a Polars DataFrame.
    
    Parameters:
        df (pl.DataFrame): Input DataFrame
        **kwargs: Additional processing parameters
    
    Returns:
        pl.DataFrame: Processed DataFrame
    """
    # Validate input
    if df.is_empty():
        return df
    
    # Process the DataFrame
    result = df.with_columns(...)
    
    return result
```

### Text Processing
```python
def process_text(text: str, language: str = 'en', **kwargs) -> list:
    """
    Process text with language-specific handling.
    
    Parameters:
        text (str): Input text
        language (str): Language code ('en' or 'th')
        **kwargs: Additional processing parameters
    
    Returns:
        list: Processed text tokens or features
    """
    # Validate language
    if language not in ['en', 'th']:
        raise ValueError(f"Unsupported language: {language}")
    
    # Language-specific processing
    if language == 'th':
        # Thai processing with lazy import
        pass
    else:
        # English processing
        pass
    
    return result
```

### Visualization Functions
```python
def create_visualization(data, **kwargs):
    """
    Create a visualization with configurable options.
    
    Parameters:
        data: Input data for visualization
        **kwargs: Visualization parameters
    
    Returns:
        matplotlib.figure.Figure: Generated figure
    """
    # Lazy import for visualization dependencies
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("matplotlib is required for visualization")
    
    # Create visualization
    fig, ax = plt.subplots()
    # ... visualization code ...
    
    return fig
```

## Future Development

### Planned Enhancements
- **Machine Learning Module**: Add functions for model evaluation, feature selection
- **More Visualizations**: Expand beyond word clouds
- **Additional Languages**: Support more languages beyond Thai and English
- **Performance Optimization**: Improve existing functions
- **Testing Framework**: Add comprehensive test suites

### Extension Guidelines
- **Backward Compatibility**: Maintain compatibility with existing code
- **Gradual Enhancement**: Add features incrementally
- **User Feedback**: Consider how new features will be used
- **Documentation**: Always update documentation with new features

## Communication Guidelines

### When Helping Users
1. **Understand Context**: This is a personal utility library
2. **Focus on Practicality**: Prioritize working solutions over theoretical perfection
3. **Consider Thai Language**: Many functions have Thai language support
4. **Suggest Improvements**: Recommend enhancements that fit the project's scope
5. **Provide Examples**: Always include working code examples
6. **Explain Trade-offs**: Discuss pros and cons of different approaches

### Code Review Comments
- **Constructive**: Focus on improvement, not criticism
- **Specific**: Point out exact issues and suggest solutions
- **Educational**: Explain why certain patterns are preferred
- **Consistent**: Follow the same standards for all code

These guidelines help maintain the quality and consistency of the Spellbook project while ensuring it remains a useful personal utility library.

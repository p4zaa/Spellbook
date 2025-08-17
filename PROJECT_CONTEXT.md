# Project Context - Spellbook

## Background and Motivation

**Spellbook** was created by Pathompong Muangthong as a personal utility library to address common challenges encountered in data science and NLP projects. The project emerged from the need to have a centralized collection of reusable, well-tested functions that could be easily imported and used across different projects.

### Why This Project Exists

1. **Personal Productivity**: Instead of rewriting common data processing functions for each project, having a centralized library saves time and ensures consistency.

2. **Code Quality**: By maintaining a single source of truth for utility functions, the code quality improves over time through iterative refinement.

3. **Thai Language Support**: Many existing libraries don't have good support for Thai language processing, so custom functions were developed to fill this gap.

4. **Multilabel Classification**: The project includes specialized functions for handling multilabel classification tasks, which are common in real-world applications but not well-supported by standard libraries.

5. **Learning and Documentation**: The project serves as a learning tool and documentation of solutions to common data science problems.

## Development Philosophy

### Personal Use First
- Functions are designed to solve real problems encountered in actual projects
- Emphasis is on practical utility rather than theoretical completeness
- The library evolves based on personal needs and project requirements

### Modular and Extensible
- Clear separation of concerns with focused modules
- Easy to add new functions without affecting existing code
- Consistent patterns make the codebase predictable and maintainable

### Quality Over Quantity
- Each function is designed to be robust and well-documented
- Comprehensive error handling with helpful error messages
- Functions are tested in real-world scenarios before being added

### Dependency Management
- Lazy imports keep the package lightweight
- Optional dependencies allow users to install only what they need
- Clear separation between core and optional functionality

## Key Problem Domains

### Data Preprocessing Challenges
- **Complex DataFrame Structures**: Many datasets have multiple header rows or complex structures that need flattening
- **Multilabel Data**: Handling datasets where each row can have multiple labels requires special processing
- **Encoding Issues**: Converting categorical and multilabel data to formats suitable for machine learning

### Text Processing Needs
- **Multi-language Support**: Working with both Thai and English text requires different processing approaches
- **Tokenization**: Proper tokenization is crucial for NLP tasks, especially for Thai text
- **Stopword Handling**: Configurable stopword removal for different languages and use cases

### Visualization Requirements
- **Text-based Visualizations**: Word clouds and other text visualizations are common in NLP projects
- **Language-specific Rendering**: Thai text requires special fonts and rendering considerations
- **Presentation Quality**: Visualizations need to be suitable for presentations and reports

### File Management
- **Batch Processing**: Automating file operations for data loading workflows
- **Format Flexibility**: Supporting various file formats and extensions
- **Path Management**: Handling file paths across different operating systems

## Technical Decisions

### Why Polars?
- **Performance**: Polars is significantly faster than pandas for many operations
- **Memory Efficiency**: Better memory management for large datasets
- **Modern API**: More intuitive and consistent API design
- **Type Safety**: Better support for type hints and validation

### Why Lazy Imports?
- **Lightweight**: Users can install only the dependencies they need
- **Flexibility**: Different users have different requirements
- **Avoiding Conflicts**: Prevents dependency conflicts in different environments
- **Better Error Messages**: Clear guidance on what needs to be installed

### Why Modular Structure?
- **Clarity**: Easy to understand what each module does
- **Maintainability**: Changes in one module don't affect others
- **Extensibility**: Easy to add new modules or functions
- **Import Organization**: Clear import patterns make code more readable

## Common Use Cases

### Data Science Workflows
1. **Data Loading**: Use file utilities to load data from various sources
2. **Data Cleaning**: Use DataFrame functions to clean and structure data
3. **Feature Engineering**: Use encoding functions to prepare features for ML
4. **Model Preparation**: Use splitting functions to prepare train/test sets
5. **Text Analysis**: Use text processing for NLP tasks
6. **Visualization**: Use viz functions to create presentations and reports

### Multilabel Classification Projects
- **Social Media Analysis**: Analyzing posts with multiple tags or categories
- **Document Classification**: Categorizing documents with multiple topics
- **Product Tagging**: Tagging products with multiple attributes
- **Content Recommendation**: Systems that need to handle multiple labels per item

### Thai Language Projects
- **Thai Social Media Analysis**: Processing Thai social media content
- **Thai Document Processing**: Analyzing Thai documents and reports
- **Thai Text Classification**: Categorizing Thai text content
- **Bilingual Projects**: Projects involving both Thai and English text

## Evolution and Future Direction

### Current State
- Core data processing functions are well-established
- Text processing with Thai language support is functional
- Basic visualization capabilities are in place
- File utilities provide essential functionality

### Planned Enhancements
- **Machine Learning Utilities**: Add functions for model evaluation, feature selection, etc.
- **More Visualizations**: Expand visualization capabilities beyond word clouds
- **Performance Optimization**: Improve performance of existing functions
- **Additional Language Support**: Extend beyond Thai and English
- **Testing Framework**: Add comprehensive test suites

### Extension Areas
- **Deep Learning Integration**: Functions for working with deep learning models
- **API Utilities**: Functions for working with external APIs
- **Database Integration**: Utilities for database operations
- **Cloud Integration**: Functions for cloud-based data processing

## Lessons Learned

### What Works Well
- **Modular Design**: Makes the codebase easy to understand and extend
- **Lazy Imports**: Provides flexibility without complexity
- **Comprehensive Documentation**: Makes functions easy to use correctly
- **Error Handling**: Helps users understand and fix issues quickly

### Challenges Addressed
- **Dependency Management**: Lazy imports solve the problem of optional dependencies
- **Code Reusability**: Centralized functions prevent code duplication
- **Language Support**: Custom functions fill gaps in existing libraries
- **Performance**: Choice of libraries like Polars addresses performance needs

### Best Practices Established
- **Function Design**: Clear inputs, outputs, and error handling
- **Documentation**: Comprehensive docstrings with examples
- **Naming Conventions**: Consistent and descriptive function names
- **Code Organization**: Logical grouping of related functions

This context helps understand why certain decisions were made and how the project fits into the broader data science ecosystem.

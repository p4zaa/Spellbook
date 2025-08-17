"""
Text tokenization utilities for Spellbook.

This module provides functions for:
- Thai and English text tokenization
- Stopword handling
- Language-specific text processing
"""

import nltk

# Download NLTK data for English tokenization (if not already installed)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


def tokenize_text(text: str, language: str = 'th', keep_stopwords: bool = True, keep_spaces: bool = False, engine: str = 'newmm') -> list:
    """
    Tokenizes text based on the specified language and handles stopwords and spaces.

    Parameters:
    text (str): The input text to tokenize.
    language (str): The language of the text ('th' for Thai, 'en' for English).
    keep_stopwords (bool): Whether to keep or drop stopwords. True keeps stopwords, False drops them.
    keep_spaces (bool): Whether to keep space characters in the output. False removes them (default).
    engine (str): The tokenizer engine for Thai text ('newmm', 'longest', 'lucene').

    Returns:
    list: A list of tokenized words.

    Raises:
    ValueError: If the language is not 'th' or 'en'.
    ImportError: If required dependencies are not installed.
    """
    # Lazy imports - only import when needed
    if language == 'th':
        try:
            from pythainlp.tokenize import Tokenizer as th_tokenizer
            from pythainlp.corpus import thai_stopwords
        except ImportError:
            raise ImportError(
                "PyThaiNLP is required for Thai text processing. "
                "Install it with: pip install pythainlp"
            )
        
        _tokenizer = th_tokenizer(custom_dict=None, engine=engine)
        words = _tokenizer.word_tokenize(text)  # Tokenize Thai text
        
        # Stopwords handling
        stop_words = thai_stopwords()
        
    elif language == 'en':
        try:
            from nltk.tokenize import word_tokenize as en_tokenizer
            from nltk.corpus import stopwords
        except ImportError:
            raise ImportError(
                "NLTK is required for English text processing. "
                "Install it with: pip install nltk"
            )
        
        words = en_tokenizer(text)  # Tokenize English text using NLTK
        
        # Stopwords handling
        stop_words = set(stopwords.words('english'))
        
    else:
        raise ValueError("Language must be 'th' for Thai or 'en' for English.")

    # Remove stopwords if keep_stopwords is False
    if not keep_stopwords:
        words = [word for word in words if word.lower() not in stop_words]

    # Remove space characters if keep_spaces is False
    if not keep_spaces:
        words = [word for word in words if word.strip() != '']

    return words

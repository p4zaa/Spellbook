import matplotlib.pyplot as plt
import nltk
from wordcloud import WordCloud
from pythainlp.tokenize import Tokenizer as th_tokenizer  # Requires PyThaiNLP for Thai tokenization
from nltk.tokenize import word_tokenize as en_tokenizer  # For English tokenization
from nltk.corpus import stopwords
from pythainlp.corpus import thai_stopwords
from pathlib import Path

# Download NLTK data for English tokenization (if not already installed)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

def tokenize_text(text: str, language: str = 'th', keep_stopwords: bool = True, engine: str = 'newmm') -> list:
    """
    Tokenizes text based on the specified language and handles stopwords.

    Parameters:
    text (str): The input text to tokenize.
    language (str): The language of the text ('th' for Thai, 'en' for English).
    keep_stopwords (bool): Whether to keep or drop stopwords. True keeps stopwords, False drops them.
    engine (str): The tokenizer engine for Thai text ('newmm', 'longest', 'lucene').

    Returns:
    list: A list of tokenized words.

    Raises:
    ValueError: If the language is not 'th' or 'en'.
    """
    # Tokenize the text based on the specified language
    if language == 'th':
        _tokenizer = th_tokenizer(custom_dict=None, engine=engine)
        words = _tokenizer.word_tokenize(text)  # Tokenize Thai text
    elif language == 'en':
        words = en_tokenizer(text)  # Tokenize English text using NLTK
    else:
        raise ValueError("Language must be 'th' for Thai or 'en' for English.")
    
    # Stopwords handling
    if language == 'th':
        stop_words = thai_stopwords()
    else:
        stop_words = set(stopwords.words('english'))

    # Remove stopwords if keep_stopwords is False
    if not keep_stopwords:
        words = [word for word in words if word.lower() not in stop_words]

    return words
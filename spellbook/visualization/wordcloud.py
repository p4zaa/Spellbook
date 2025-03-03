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

FONT_FOLDER = Path(__file__).parent / 'fonts'

def plot_wordcloud(text: str, language: str = 'th', keep_stopwords: bool = True, font_path: str = FONT_FOLDER / 'THSarabunNew.ttf', engine: str = 'newmm', figsize=(10, 6), interpolation="bilinear", title: str = None, width: int = 800, height: int = 400, save_path: str = None, transparent=True, **wordcloud_kwargs):
    """
    Plots a word cloud from text with language-specific tokenization and stopword handling.

    Parameters:
    text (str): The input text.
    language (str): The language of the text ('th' for Thai, 'en' for English).
    keep_stopwords (bool): Whether to keep or drop stopwords. True keeps stopwords, False drops them.
    font_path (str): Path to a Thai font file (default: TH Sarabun New).
    engine (str): The tokenizer engine for Thai text ('newmm', 'longest', 'lucene').
    figsize (tuple): Figure size for the plot (default: (10, 6)).
    interpolation (str): Interpolation method for displaying the image (default: "bilinear").
    title (str): The title of the word cloud (default: None, which means no title).
    width (int): The width of the word cloud (default: 800).
    height (int): The height of the word cloud (default: 400).
    save_path (str): Path to save the word cloud image (default: None, which means the image is not saved).
    wordcloud_kwargs: Additional keyword arguments to customize the WordCloud instance (e.g., max_words, contour_color).
    """
    #print(FONT_FOLDER)
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

    processed_text = " ".join(words)  # Join words for wordcloud input

    # Generate word cloud with additional keyword arguments
    wordcloud = WordCloud(
        font_path=font_path,  # Use Thai font if specified
        #background_color="white",
        width=width,  # Set width for the word cloud
        height=height,  # Set height for the word cloud
        mode='RGBA',
        collocations=False,
        normalize_plurals=True,
        include_numbers=False,
        regexp=r"[\u0E00-\u0E7Fa-zA-Z']+",  # Match Thai or English words
        #colormap="viridis",
        **wordcloud_kwargs  # Pass additional parameters to WordCloud
    ).generate(processed_text)

    # Plot word cloud
    plt.figure(figsize=figsize)
    plt.imshow(wordcloud, interpolation=interpolation)
    plt.axis("off")  # Hide axes
    
    # Add title if it's not None
    if title:
        plt.title(title)
    
    # Save the figure if save_path is specified
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', transparent=transparent)  # Save image with tight bounding box to avoid clipping
    
    plt.show()
    return wordcloud
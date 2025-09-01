from setuptools import setup, find_packages

# Read README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="spellbook",
    version="0.1.0",
    packages=find_packages(include=["spellbook", "spellbook.*"]),
    
    # Core dependencies - minimal set for basic functionality
    install_requires=[
        "numpy>=1.20.0",
        "polars>=0.20.0",
        "fastexcel>=0.10.0",
        "scikit-learn>=1.0.0",
    ],
    
    # Optional dependency groups
    extras_require={
        "viz": [
            "matplotlib>=3.5.0",
            "wordcloud>=1.8.0",
        ],
        "text": [
            "pythainlp>=3.0.0",
            "nltk>=3.7",
        ],
        "scraping": [
            "selenium>=4.0.0",
            "crawl4ai>=0.1.0",
            "requests>=2.25.0",
            "httpx>=0.20.0",
        ],
        "network": [
            "networkx>=2.6.0",
        ],
        "utils": [
            "bloxs>=0.1.0",
        ],
        "full": [
            "matplotlib>=3.5.0",
            "wordcloud>=1.8.0",
            "pythainlp>=3.0.0",
            "nltk>=3.7",
            "selenium>=4.0.0",
            "crawl4ai>=0.1.0",
            "requests>=2.25.0",
            "httpx>=0.20.0",
            "networkx>=2.6.0",
            "bloxs>=0.1.0",
        ],
        "dev": [
            "matplotlib>=3.5.0",
            "wordcloud>=1.8.0",
            "pythainlp>=3.0.0",
            "nltk>=3.7",
            "selenium>=4.0.0",
            "crawl4ai>=0.1.0",
            "requests>=2.25.0",
            "httpx>=0.20.0",
            "networkx>=2.6.0",
            "bloxs>=0.1.0",
            "pytest>=6.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
        ],
    },
    
    # Package data
    package_data={
        "spellbook.viz.fonts": ["*.ttf", "*.otf", "*.woff", "*.woff2"],
    },
    include_package_data=True,
    
    # Metadata
    description="A collection of useful data science and NLP utilities with intelligent dependency management.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/p4zaa/SpellBook",
    author="Pathompong Muangthong",
    author_email="pathompong.workspace@gmail.com",
    license="MIT",
    
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Data Scientists",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Entry points for lazy loading
    entry_points={
        "console_scripts": [
            "spellbook=spellbook.cli:main",
        ],
    },
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/p4zaa/SpellBook/issues",
        "Source": "https://github.com/p4zaa/SpellBook",
        "Documentation": "https://github.com/p4zaa/SpellBook#readme",
    },
    
    # Keywords
    keywords="data-science nlp machine-learning text-processing visualization web-scraping",
    
    # Additional metadata
    maintainer="Pathompong Muangthong",
    maintainer_email="pathompong.workspace@gmail.com",
)
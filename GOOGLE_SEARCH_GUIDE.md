# Google Search with Selenium Guide

This guide explains how to use the new Google search function that utilizes Selenium with `headless=False` to see the browser in action.

## Features

- **Visual Browser**: See the browser window as it performs searches
- **CAPTCHA Handling**: Automatic detection and manual solving support
- **Flexible Search**: Support for keywords, site restrictions, and year filters
- **URL Cleaning**: Automatic removal of Google redirects
- **Anti-Detection**: Built-in measures to avoid bot detection
- **Consistent Schema**: Uses the same data schema as existing search functions
- **Multi-Page Scraping**: Automatically clicks next button to scrape all pages
- **Flexible Limits**: Set max_results and max_pages limits (None for no limit)

## Installation

1. Install the required dependencies:
```bash
pip install selenium
```

2. Install Chrome browser if not already installed

3. Install ChromeDriver:
   - **macOS**: `brew install chromedriver`
   - **Windows**: Download from https://chromedriver.chromium.org/
   - **Linux**: `sudo apt-get install chromium-chromedriver`

## Basic Usage

### Simple Search

```python
from spellbook.scraper.google_search_basic import google_search_selenium

# Basic search with pagination
results = google_search_selenium(
    keyword="travel card",
    site="pantip.com",
    year=2024,
    max_results=20,    # Get up to 20 results
    max_pages=5,       # Scrape up to 5 pages
    headless=False     # See the browser window
)

# Print results
for result in results:
    print(f"Title: {result['title'] or 'No title'}")
    print(f"URL: {result['url'] or 'No URL'}")
    print(f"Date: {result['date_string'] or 'No date'}")
    print(f"Content: {result['related_content'] or 'No content'}")
    print()
```

### URL-Only Search

```python
from spellbook.scraper.google_search_basic import google_search_simple

# Get just URLs with pagination
urls = google_search_simple(
    keyword="python selenium",
    site="stackoverflow.com",
    year=2024,
    max_results=15,    # Get up to 15 URLs
    max_pages=3        # Scrape up to 3 pages
)

for url in urls:
    print(url)
```

## Data Schema

The function returns results in the same schema as the existing search functions:

```python
{
    "url": "https://example.com/page",  # Cleaned URL (None if not found)
    "title": "Page Title",              # Page title (None if not found)
    "related_content": "Full text...",  # All text content (None if not found)
    "date_string": "2024-01-15"         # Date if available (None if not found)
}
```

## Search Query Construction

The function constructs search queries similar to your example:

```python
keyword = 'travel card'
site = 'pantip.com'
year = 2024

# Results in URL like:
# https://www.google.com/search?q=site:pantip.com+after:2024+travel+card&as_epq=travel+card
```

## Parameters

### `google_search_selenium()`

- **`keyword`** (str): Search keyword(s)
- **`site`** (str, optional): Site restriction (e.g., "pantip.com")
- **`year`** (int, optional): Year filter (e.g., 2024)
- **`max_results`** (int, optional): Maximum number of results (default: 20, None for no limit)
- **`max_pages`** (int, optional): Maximum number of pages to scrape (default: None, None for no limit)
- **`headless`** (bool): Run headless (default: False)
- **`browser_driver_path`** (str, optional): Path to Chrome driver
- **`wait_time`** (int): Time to wait for page elements (default: 10)

### `google_search_simple()`

- **`keyword`** (str): Search keyword(s)
- **`site`** (str, optional): Site restriction
- **`year`** (int, optional): Year filter
- **`max_results`** (int, optional): Maximum number of URLs (default: 10, None for no limit)
- **`max_pages`** (int, optional): Maximum number of pages to scrape (default: None, None for no limit)

## Pagination

The function automatically handles pagination by clicking the next button:

1. **Next Button Detection**: Uses `document.querySelector("a#pnnext")` to find the next button
2. **Automatic Clicking**: Clicks the next button and waits for page load
3. **CAPTCHA Handling**: Detects and handles CAPTCHA on each page
4. **Flexible Limits**: 
   - Set `max_results=None` for unlimited results
   - Set `max_pages=None` to scrape until no more pages
   - Set specific limits to control scraping depth

## CAPTCHA Handling

The function uses the advanced captcha_detector module for comprehensive CAPTCHA detection:

1. **Advanced Detection**: Uses domain-specific patterns and HTML content analysis
2. **Multiple CAPTCHA Types**: Detects various CAPTCHA systems (reCAPTCHA, Cloudflare, etc.)
3. **Manual Solving**: Keeps browser window open for manual CAPTCHA solving
4. **Auto-Continue**: Automatically continues after CAPTCHA is solved
5. **Timeout**: 5-minute timeout for CAPTCHA solving
6. **No Results Detection**: Also detects when no search results are available

## Anti-Detection Features

- **User Agent**: Realistic browser user agent
- **WebDriver Removal**: Removes webdriver properties
- **Automation Flags**: Disables automation indicators
- **Random Delays**: Built-in delays to mimic human behavior
- **Advanced CAPTCHA Detection**: Uses sophisticated patterns instead of simple keyword matching
- **No Results Detection**: Automatically stops when no more results are available

## Example Use Cases

### 1. Research on Specific Sites

```python
# Search for Python tutorials on specific sites
results = google_search_selenium(
    keyword="python tutorial",
    site="realpython.com",
    year=2024,
    max_results=15
)
```

### 2. Recent Content Search

```python
# Find recent articles about machine learning
results = google_search_selenium(
    keyword="machine learning",
    year=2024,
    max_results=20
)
```

### 3. Site-Specific Research

```python
# Search for web scraping projects on GitHub
results = google_search_selenium(
    keyword="web scraping",
    site="github.com",
    max_results=10
)
```

### 4. Unlimited Scraping

```python
# Scrape all available results (no limits)
results = google_search_selenium(
    keyword="python tutorial",
    max_results=None,  # No limit on results
    max_pages=None,    # No limit on pages
    headless=True      # Run headless for large scraping
)
```

### 5. Limited Page Scraping

```python
# Scrape only first 3 pages regardless of results
results = google_search_selenium(
    keyword="machine learning",
    max_pages=3,       # Only 3 pages
    max_results=None   # All results from those pages
)
```

## Troubleshooting

### ChromeDriver Issues

```bash
# Check ChromeDriver version
chromedriver --version

# Check Chrome browser version
google-chrome --version

# Make sure versions are compatible
```

### Common Errors

1. **"ChromeDriver executable needs to be in PATH"**
   - Install ChromeDriver or provide path via `browser_driver_path`

2. **"CAPTCHA detected"**
   - Solve CAPTCHA manually in the browser window
   - Function will continue automatically after solving

3. **"No results found"**
   - Try different keywords or remove site restrictions
   - Check if the search query is too specific

### Performance Tips

1. **Use headless mode** for production: `headless=True`
2. **Adjust wait times** based on your internet speed
3. **Limit max_results** to avoid long processing times
4. **Use site restrictions** to get more relevant results

## Running the Test

```bash
# Run the test script
python test_google_search_selenium.py
```

This will demonstrate the function with the example search parameters and show you how the browser behaves.

## Integration with Existing Code

The new function can be used alongside existing search functions:

```python
from spellbook.scraper import search, google_search_basic

# Use crawl4ai-based search (existing)
urls_crawl4ai = await search.search_google("python", max_results=10)

# Use Selenium-based search (new)
urls_selenium = google_search_basic.google_search_simple("python", max_results=10)
```

## Security Notes

- The function respects Google's terms of service
- Built-in rate limiting and delays
- Manual CAPTCHA solving when required
- No automated CAPTCHA solving to comply with terms

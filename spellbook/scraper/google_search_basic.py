import time
import re
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode, quote_plus
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from .captcha_detector import detect_captcha, detect_no_results


def google_search_selenium(
    keyword: str,
    site: Optional[str] = None,
    year: Optional[int] = None,
    max_results: Optional[int] = None,
    max_pages: Optional[int] = None,
    headless: bool = False,
    browser_driver_path: Optional[str] = None,
    wait_time: int = 10,
    captcha_max_wait_time: int = 1800
) -> List[Dict[str, Any]]:
    """
    Perform Google search using Selenium with headless=False to see the browser.
    
    Args:
        keyword: Search keyword(s)
        site: Optional site restriction (e.g., "pantip.com")
        year: Optional year filter (e.g., 2024)
        max_results: Maximum number of results to return (None for no limit)
        max_pages: Maximum number of pages to scrape (None for no limit)
        headless: Whether to run headless (default False to see browser)
        browser_driver_path: Optional path to Chrome driver
        wait_time: Time to wait for page elements to load
        captcha_max_wait_time: Maximum time to wait for CAPTCHA solution in seconds (default 1800 = 30 minutes)
        
    Returns:
        List of dictionaries containing search results with 'url', 'title', 'related_content', 'date_string' keys
        (missing elements are set to None)
        
    Note:
        - If max_results is None, no limit on number of results
        - If max_pages is None, continues until no more next button
        - Scrapes all elements on each page and combines results
    """
    
    # Construct search query similar to the example
    keyword_mod = keyword.lower().replace(' ', '+')
    
    # Build the search URL
    query_parts = []
    
    # Add site restriction if provided
    if site:
        query_parts.append(f"site:{site}")
    
    # Add year filter if provided
    if year:
        query_parts.append(f"after:{year}")
    
    # Add the main keyword
    query_parts.append(keyword_mod)
    
    # Construct the full query
    full_query = " ".join(query_parts)
    
    # Build the Google search URL
    params = {
        "q": full_query,
        "as_epq": keyword_mod  # Exact phrase query
    }
    
    google_search_url = f"https://www.google.com/search?{urlencode(params)}"
    
    print(f"🔍 Searching Google with URL: {google_search_url}")
    print(f"📝 Query: {full_query}")
    
    # Setup Chrome options
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
    
    # Add other useful options
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Set user agent to avoid detection
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    results = []
    
    try:
        # Initialize the driver
        if browser_driver_path:
            service = Service(browser_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        # Execute script to remove webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"🌐 Opening browser and navigating to Google search...")
        
        # Navigate to the search URL
        driver.get(google_search_url)
        
        # Wait for search results to load
        wait = WebDriverWait(driver, wait_time)
        
        try:
            # Wait for search results container
            wait.until(EC.presence_of_element_located((By.ID, "search")))
            print("✅ Search results loaded successfully")
        except TimeoutException:
            print("⚠️  Timeout waiting for search results. Checking if page loaded...")
            
            # Check if we're on a CAPTCHA page using the captcha detector
            is_captcha, captcha_type, details = detect_captcha(
                url=driver.current_url,
                html_content=driver.page_source,
                domain="google.com"
            )

            
            if is_captcha:
                print(f"🚨 CAPTCHA detected: {captcha_type}")
                print(f"   Details: {details}")
                print(f"   URL: {driver.current_url}")
                print("⏳ Waiting for CAPTCHA to be solved...")
                
                # Wait for user to solve CAPTCHA
                wait_interval = 5    # Check every 5 seconds
                waited_time = 0
                
                while waited_time < captcha_max_wait_time:
                    time.sleep(wait_interval)
                    waited_time += wait_interval
                    
                    # Check if we're still on a CAPTCHA page
                    is_still_captcha, _, _ = detect_captcha(
                        url=driver.current_url,
                        html_content=driver.page_source,
                        domain="google.com"
                    )
                    
                    if not is_still_captcha:
                        print("✅ CAPTCHA appears to be solved! Continuing...")
                        break
                    
                    if waited_time % 30 == 0:  # Print status every 30 seconds
                        print(f"⏰ Still waiting for CAPTCHA solution... ({waited_time}s elapsed)")
                
                if waited_time >= captcha_max_wait_time:
                    print("⚠️  Timeout waiting for CAPTCHA. Continuing anyway...")
        
        # Start pagination loop
        current_page = 1
        has_more_pages = True
        
        while has_more_pages:
            print(f"📄 Processing page {current_page}...")
            
            # Extract search results from current page
            print("📄 Extracting search results from current page...")
            
            # Find all search result containers
            # Google search results are typically in divs with class 'g' or similar
            result_elements = driver.find_elements(By.CSS_SELECTOR, "div.g, div[data-testid='result'], .MjjYud")
            
            if not result_elements:
                # Try alternative selectors
                result_elements = driver.find_elements(By.CSS_SELECTOR, "#rso > div, .yuRUbf")
            
            print(f"🔍 Found {len(result_elements)} result elements on page {current_page}")
            
            # Check for no results using the captcha detector
            has_no_results, no_results_type, no_results_details = detect_no_results(
                html_content=driver.page_source,
                domain="google.com"
            )
            
            if has_no_results:
                print(f"⚠️  No results detected: {no_results_type}")
                print(f"   Details: {no_results_details}")
                print(f"   Stopping pagination as no more results are available")
                break
            
            # Extract results from current page
            page_results = []
            for i, element in enumerate(result_elements):
                try:
                    result_data = {}
                    
                    # Extract URL (primary field)
                    try:
                        url_element = element.find_element(By.CSS_SELECTOR, "a")
                        result_data['url'] = url_element.get_attribute('href')
                    except NoSuchElementException:
                        result_data['url'] = None
                    
                    # Extract title
                    try:
                        title_element = element.find_element(By.CSS_SELECTOR, "h3")
                        result_data['title'] = title_element.text.strip()
                    except NoSuchElementException:
                        result_data['title'] = None
                    
                    # Extract related_content (all text content from the element)
                    try:
                        # Get all text content from the element
                        related_content = element.text.strip()
                        result_data['related_content'] = related_content
                    except Exception:
                        result_data['related_content'] = None
                    
                    # Extract date_string
                    try:
                        date_element = element.find_element(By.CSS_SELECTOR, "div > span.YrbPuc > span")
                        result_data['date_string'] = date_element.text.strip()
                    except NoSuchElementException:
                        # Try fallback selector for date
                        try:
                            date_element = element.find_element(By.CSS_SELECTOR, "div.byrV5b > cite")
                            result_data['date_string'] = date_element.text.strip()
                        except NoSuchElementException:
                            result_data['date_string'] = None
                    
                    # Clean the URL (remove Google redirects)
                    if result_data['url']:
                        result_data['url'] = _clean_google_url(result_data['url'])
                    
                    # Only add if we have a valid URL
                    if result_data['url'] and not result_data['url'].startswith('https://www.google.com'):
                        page_results.append(result_data)
                
                except Exception as e:
                    print(f"⚠️  Error extracting result {i+1} on page {current_page}: {e}")
                    continue
            
            # Add page results to total results
            results.extend(page_results)
            print(f"✅ Added {len(page_results)} results from page {current_page}")
            print(f"📊 Total results so far: {len(results)}")
            
            # Check if we've reached max_results limit
            if max_results is not None and len(results) >= max_results:
                print(f"🎯 Reached max_results limit ({max_results})")
                results = results[:max_results]
                break
            
            # Check if we've reached max_pages limit
            if max_pages is not None and current_page >= max_pages:
                print(f"📄 Reached max_pages limit ({max_pages})")
                break
            
            # Try to find and click next button
            try:
                # Wait a bit for page to fully load
                time.sleep(2)
                
                # Look for next button using the provided selector
                next_button = driver.find_element(By.CSS_SELECTOR, "a#pnnext")
                
                # Check if next button is clickable
                if next_button.is_enabled() and next_button.is_displayed():
                    print(f"➡️  Clicking next button to go to page {current_page + 1}...")
                    
                    # Scroll to next button to ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    
                    # Click the next button
                    next_button.click()
                    
                    # Wait a moment for page to start loading
                    time.sleep(3)
                    
                    # Check for CAPTCHA immediately after clicking next button
                    print(f"🔍 Checking for CAPTCHA after clicking next button...")
                    #print(f"   Current URL: {driver.current_url}")
                    #print(f"   Page title: {driver.title}")
                    
                    is_captcha, captcha_type, details = detect_captcha(
                        url=driver.current_url,
                        html_content=driver.page_source,
                        domain="google.com"
                    )
                    
                    # Additional check for CAPTCHA elements
                    '''if not is_captcha:
                        captcha_elements = driver.find_elements(By.CSS_SELECTOR, 
                            "iframe[src*='recaptcha'], .g-recaptcha, #recaptcha, .captcha, [class*='captcha'], [id*='captcha']")
                        if captcha_elements:
                            print(f"   ⚠️  Found {len(captcha_elements)} CAPTCHA elements on page")
                            is_captcha = True
                            captcha_type = "visual_elements"
                            details = f"Found {len(captcha_elements)} CAPTCHA elements on page"
                    
                    # Check for common CAPTCHA indicators in page source
                    if not is_captcha:
                        page_source_lower = driver.page_source.lower()
                        captcha_keywords = ["captcha", "recaptcha", "verify you are human", "robot check", "unusual traffic"]
                        found_keywords = [kw for kw in captcha_keywords if kw in page_source_lower]
                        if found_keywords:
                            print(f"   ⚠️  Found CAPTCHA keywords: {found_keywords}")
                            is_captcha = True
                            captcha_type = "keyword_detection"
                            details = f"Found CAPTCHA keywords: {', '.join(found_keywords)}"'''
                    
                    if is_captcha:
                        print(f"🚨 CAPTCHA detected on new page: {captcha_type}")
                        print(f"   Details: {details}")
                        print(f"   URL: {driver.current_url}")
                        print("⏳ Waiting for CAPTCHA to be solved...")
                        print("💡 Please solve the CAPTCHA in the browser window")
                        
                        # Wait for user to solve CAPTCHA
                        wait_interval = 5    # Check every 5 seconds
                        waited_time = 0
                        
                        while waited_time < captcha_max_wait_time:
                            time.sleep(wait_interval)
                            waited_time += wait_interval
                            
                            # Check if we're still on a CAPTCHA page
                            is_still_captcha, _, _ = detect_captcha(
                                url=driver.current_url,
                                html_content=driver.page_source,
                                domain="google.com"
                            )
                            
                            # Additional check for CAPTCHA elements
                            '''if not is_still_captcha:
                                captcha_elements = driver.find_elements(By.CSS_SELECTOR, 
                                    "iframe[src*='recaptcha'], .g-recaptcha, #recaptcha, .captcha, [class*='captcha'], [id*='captcha']")
                                if captcha_elements:
                                    is_still_captcha = True'''
                            
                            if not is_still_captcha:
                                print("✅ CAPTCHA appears to be solved! Continuing...")
                                break
                            
                            if waited_time % 30 == 0:  # Print status every 30 seconds
                                print(f"⏰ Still waiting for CAPTCHA solution... ({waited_time}s elapsed)")
                                print("💡 Please solve the CAPTCHA in the browser window")
                        
                        if waited_time >= captcha_max_wait_time:
                            print("⚠️  Timeout waiting for CAPTCHA. Continuing anyway...")
                    
                    # Only wait for search results if we're not on a CAPTCHA page
                    if not is_captcha:
                        try:
                            wait.until(EC.presence_of_element_located((By.ID, "search")))
                            print("✅ Search results loaded successfully")
                        except TimeoutException:
                            print("⚠️  Timeout waiting for search results")
                    else:
                        print("⏭️  Skipping search results wait due to CAPTCHA")
                    
                    current_page += 1
                    print(f"✅ Successfully navigated to page {current_page}")
                    
                else:
                    print("❌ Next button found but not clickable")
                    has_more_pages = False
                    
            except NoSuchElementException:
                print("❌ No next button found - reached last page")
                has_more_pages = False
                
            except Exception as e:
                print(f"⚠️  Error navigating to next page: {e}")
                has_more_pages = False
        
        print(f"✅ Successfully extracted {len(results)} total search results from {current_page} pages")
        
    except WebDriverException as e:
        print(f"❌ WebDriver error: {e}")
        print("💡 Make sure Chrome browser and ChromeDriver are installed and compatible")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        if driver:
            print("🔒 Closing browser...")
            time.sleep(3)
            driver.quit()
    
    # Apply max_results limit if specified
    if max_results is not None:
        results = results[:max_results]
    
    return results


def _clean_google_url(url: str) -> str:
    """
    Clean Google search result URLs by removing redirects and extracting the actual destination URL.
    
    Args:
        url: Raw URL from Google search results
        
    Returns:
        Cleaned URL pointing to the actual destination
    """
    if not url:
        return ""
    
    # Handle Google redirects: /url?q=<dest>
    if "google.com" in url and "/url?" in url:
        try:
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(url)
            if parsed.path == "/url":
                q_params = parse_qs(parsed.query)
                if 'q' in q_params:
                    actual_url = q_params['q'][0]
                    if actual_url.startswith(('http://', 'https://')):
                        return actual_url
        except Exception:
            pass
    
    return url


def google_search_simple(
    keyword: str,
    site: Optional[str] = None,
    year: Optional[int] = None,
    max_results: Optional[int] = None,
    max_pages: Optional[int] = None,
    captcha_max_wait_time: int = 1800
) -> List[str]:
    """
    Simple Google search that returns just URLs.
    
    Args:
        keyword: Search keyword(s)
        site: Optional site restriction
        year: Optional year filter
        max_results: Maximum number of URLs to return
        max_pages: Maximum number of pages to scrape (None for no limit)
        captcha_max_wait_time: Maximum time to wait for CAPTCHA solution in seconds (default 1800 = 30 minutes)
        
    Returns:
        List of URLs from search results
    """
    results = google_search_selenium(
        keyword=keyword,
        site=site,
        year=year,
        max_results=max_results,
        max_pages=max_pages,
        headless=False,
        captcha_max_wait_time=captcha_max_wait_time
    )
    
    return [result['url'] for result in results if result.get('url') is not None]


# Example usage function
def example_search():
    """
    Example usage of the Google search function.
    """
    print("🔍 Example Google Search with Selenium")
    print("=" * 50)
    
    # Example search similar to the provided example
    keyword = 'เกาะพะงัน'
    site = 'pantip.com'
    year = 2024
    
    results = google_search_selenium(
        keyword=keyword,
        site=site,
        year=year,
        max_results=None,  # Get up to 10 results
        max_pages=3,     # Scrape up to 3 pages
        headless=False   # Set to True if you don't want to see the browser
    )
    
    print(f"\n📊 Search Results for '{keyword}' on {site} after {year}:")
    print("-" * 50)
    
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title'] or 'No title'}")
        print(f"   URL: {result['url'] or 'No URL'}")
        print(f"   Date: {result['date_string'] or 'No date'}")
        print(f"   Content: {result['related_content'][:100] if result['related_content'] else 'No content'}...")
        print()


if __name__ == "__main__":
    example_search()

import asyncio
import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, urlparse, parse_qs, unquote

from crawl4ai import AsyncWebCrawler
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, VirtualScrollConfig
from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher, SemaphoreDispatcher
from crawl4ai import RateLimiter, CrawlerMonitor, DisplayMode

from .captcha_detector import detect_captcha, handle_captcha


def _is_jupyter_environment() -> bool:
    """Check if we're running in a Jupyter notebook environment."""
    try:
        import IPython
        return IPython.get_ipython() is not None
    except ImportError:
        return False


def _safe_create_monitor() -> Optional[CrawlerMonitor]:
    """Safely create a CrawlerMonitor, handling Jupyter notebook environments."""
    if _is_jupyter_environment():
        print("   📝 Note: CrawlerMonitor disabled in Jupyter notebook environment")
        return None
    
    try:
        return CrawlerMonitor(
            #max_visible_rows=10,
            #display_mode=DisplayMode.DETAILED
        )
    except Exception as e:
        print(f"   ⚠️  Could not initialize CrawlerMonitor: {e}")
        print("   📝 Continuing without monitoring...")
        return None


def _unique_preserve_order(items: List[str]) -> List[str]:
    seen = set()
    unique: List[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def _clean_search_result_url(raw_url: str, provider: str) -> Optional[str]:
    if not raw_url:
        return None

    try:
        parsed = urlparse(raw_url)

        # Normalize scheme-less and relative URLs
        if not parsed.scheme and raw_url.startswith("//"):
            raw_url = f"https:{raw_url}"
            parsed = urlparse(raw_url)

        # Google redirects: /url?q=<dest>
        if provider == "google":
            if (parsed.netloc.endswith("google.com") or parsed.netloc.endswith("google.co")) and parsed.path == "/url":
                q = parse_qs(parsed.query).get("q", [None])[0]
                if q and (q.startswith("http://") or q.startswith("https://")):
                    return q
            # Skip Google internal links
            if parsed.netloc.endswith("google.com"):
                return None

        # DuckDuckGo redirects: /l/?uddg=<dest>
        if provider == "duckduckgo":
            if parsed.netloc.endswith("duckduckgo.com") and parsed.path.startswith("/l/"):
                uddg = parse_qs(parsed.query).get("uddg", [None])[0]
                if uddg:
                    return unquote(uddg)
            if parsed.netloc.endswith("duckduckgo.com"):
                return None

        # Pantip: topic links may be relative
        if provider == "pantip":
            if raw_url.startswith("/topic/"):
                return f"https://pantip.com{raw_url}"
            if parsed.netloc.endswith("pantip.com") and parsed.path.startswith("/topic/") and parsed.scheme in ("http", "https"):
                return raw_url
            # Ignore non-topic links
            return None

        if parsed.scheme in ("http", "https"):
            return raw_url
    except Exception:
        return None

    return None


def _google_search_url(keyword: str, *, lang: str = "en", region: str = "us", start: int = 0, site: Optional[str] = None) -> str:
    query = f"site:{site} {keyword}" if site else keyword
    params = {
        "q": query,
        "hl": lang,
        "gl": region,
        "start": str(start),
        "num": "10",
        "pws": "0",
    }
    return f"https://www.google.com/search?{urlencode(params)}"


def _duckduckgo_search_url(keyword: str, *, lang: str = "en", region: str = "us", page: int = 1, site: Optional[str] = None) -> str:
    # Use the lightweight HTML version for easier parsing
    query = f"site:{site} {keyword}" if site else keyword
    params = {
        "q": query,
        "kl": f"{region}-{lang}",
        "s": str((page - 1) * 30),
    }
    return f"https://html.duckduckgo.com/html/?{urlencode(params)}"


def _pantip_search_url(keyword: str, *, timebias: bool = True) -> str:
    params = {
        "q": keyword,
    }
    if timebias:
        params["timebias"] = "true"
    return f"https://pantip.com/search?{urlencode(params)}"


def _google_extraction_config(max_paginate: int = 3, pagination_mode: str = "multi_window") -> CrawlerRunConfig:
    # Organic results are usually wrapped in .g under #search
    schema = {
        "baseSelector": "#rso > div[class='MjjYud'], .g", # Multiple selectors for better coverage
        "fields": [
            {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"},
            {"name": "title", "selector": "h3", "type": "text"},
            {
                "name": "related_content",
                "type": "text",
                "multiple": True
            },
            {
                "name": "date_string",
                "selector": "div > span.YrbPuc > span",
                "type": "text"
            }
        ],
    }

    virtual_scroll_config = VirtualScrollConfig(
        container_selector="html, body",
        scroll_count=10,
        scroll_by="container_height",
        wait_after_scroll=0.5
        )

    # JS code: clicks next if exists, else stops
    js_code = """
    async function paginate() {
        let nextBtn = document.querySelector("a#pnnext");
        if (nextBtn && !nextBtn.disabled) {
            nextBtn.click();
            await new Promise(r => setTimeout(r, 3000)); // wait for page load
            return true;  // tell Crawl4AI to continue
        }
        return false;     // stop when no next button
    }
    await paginate();
    """

    # JS code to go back if page has no results
    js_back_page = """
    async function goBackIfNoResults() {
        // Delay before checking
        await new Promise(r => setTimeout(r, 2000)); // wait 2 seconds before executing

        // Check if search results exist
        let hasResults = document.querySelector("#rso, .g, .MjjYud");

        if (!hasResults) {
            console.log("No results found. Going back in browser history...");
            window.history.back();  // go back to previous page
            await new Promise(r => setTimeout(r, 3000)); // wait for previous page to load
            return true;  // continue crawling after going back
        }

        return false; // results exist, no need to go back
    }

    // Call the function after initial delay
    await goBackIfNoResults();
    """

    wait_for_logic = """
    () => {
        // Check if search results exist
        const resultsExist = document.querySelector("#rso, .g, .MjjYud");

        if (resultsExist) {
            return true; // we have results, proceed
        } else {
            // No results, go back in browser history
            window.history.back();
            await new Promise(r => setTimeout(r, 10000)); // wait for previous page to load
            console.log("No results found. Going back...");
            return false; // keep waiting until a valid page is loaded
        }
    }"""

    return CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(schema=schema),
        #js_code=[js_back_page],
        #js_only=True,
        scan_full_page=True,
        magic=True,
        simulate_user=True,
        override_navigator=True,
        #virtual_scroll_config=virtual_scroll_config,
        wait_until="networkidle",  # Wait for network to be idle
        wait_for="#rso, .g, .MjjYud",  # Wait for search results to load
        # Anti-bot measures
        #check_robots_txt=True,  # Respect robots.txt
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="America/New_York"
    )

#botstuff > div > div:nth-child(3) > table > tbody > tr > td.YyVfkd.NKTSme
##botstuff > div > div:nth-child(3) > table > tbody > tr > td.YyVfkd.NKTSme > span
def _duckduckgo_extraction_config() -> CrawlerRunConfig:
    # HTML version: each result under .result, anchor is a.result__a
    schema = {
        "baseSelector": "#links .result",
        "fields": [
            {"name": "url", "selector": "a.result__a", "type": "attribute", "attribute": "href"},
            {"name": "title", "selector": "a.result__a", "type": "text"},
        ],
    }
    return CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema=schema),
                            scan_full_page=True,
                            scroll_delay=0.5,)


def _pantip_extraction_config() -> CrawlerRunConfig:
    # Grab topic links; Pantip topics follow /topic/<id>
    schema = {
        "baseSelector": "li.pt-list-item.pt-list-item__sr__no-img",
        "fields": [
            {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"},
            {"name": "date_string", "selector": "span.txt-purple-pantip-200.p-r-8.pt-sm-toggle-date-show", "type": "text"},
            {"name": "title", "selector": "h2 > a > span", "type": "text"},
            {
                "name": "related_content", 
                #"selector": "span", #"div.pt-list-item__sr__content__inner > span:nth-child(2)", 
                "type": "text",
                "multiple": True,
            },
        ],
    }

    # Configure virtual scroll
    virtual_config = VirtualScrollConfig(
        container_selector="hrml, body",          # CSS selector for scrollable container
        scroll_count=10,                    # Number of scrolls to perform
        scroll_by="container_height",       # How much to scroll each time
        wait_after_scroll=0.5               # Wait time (seconds) after each scroll
    )
    return CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema=schema), 
                            virtual_scroll_config=virtual_config,
                            scan_full_page=True,
                            scroll_delay=0.5,)


from typing import Tuple


def _get_captcha_wait_selectors(provider: str) -> str:
    """Get appropriate wait_for selectors for CAPTCHA detection based on provider."""
    if provider == "google":
        return '#search, .g, .MjjYud, [data-testid="result"], #rso, .yuRUbf'  # Google search results
    elif provider == "duckduckgo":
        return '#links, .result, .result__a, .result__title'  # DuckDuckGo search results
    elif provider == "pantip":
        return '.pt-list-item, .pt-list-item__sr__no-img, h2 > a > span, .pt-list-item__sr__content'  # Pantip topic results
    else:
        return '#search, .g, .result, .pt-list-item, h1, h2, h3'  # Generic fallback


def _create_google_dispatcher(enable_monitoring: bool = True) -> MemoryAdaptiveDispatcher:
    """Create a specialized dispatcher for Google crawling with anti-bot measures."""
    
    # Rate limiter optimized for Google
    rate_limiter = RateLimiter(
        base_delay=(3.0, 7.0),      # Random delay between 3-7 seconds (more conservative)
        max_delay=120.0,            # Maximum backoff delay of 2 minutes
        max_retries=2,              # Retry up to 2 times on rate limits
        rate_limit_codes=[429, 503, 403]  # Include 403 (Forbidden) for Google
    )
    
    # Memory adaptive dispatcher with conservative settings
    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=75.0,  # Lower threshold for Google (more conservative)
        check_interval=2.0,             # Check memory every 2 seconds
        max_session_permit=3,           # Limit to 3 concurrent sessions for Google
        rate_limiter=rate_limiter,
        memory_wait_timeout=300.0       # Wait up to 5 minutes for memory to free up
    )
    
    # Add monitoring if enabled
    if enable_monitoring:
        monitor = _safe_create_monitor()
        if monitor:
            dispatcher.monitor = monitor
    
    return dispatcher

def _extraction_config_for_url(search_url: str) -> Tuple[CrawlerRunConfig, Optional[str]]:
    """Infer the extraction config and provider from the base search URL."""
    parsed = urlparse(search_url)
    host = (parsed.hostname or "").lower()
    path = parsed.path or ""

    # Pantip search pages
    if host.endswith("pantip.com") and path.startswith("/search"):
        return _pantip_extraction_config(), "pantip"

    # Google web search pages
    if ("google." in host) and path.startswith("/search"):
        return _google_extraction_config(), "google"

    # DuckDuckGo html search pages
    if host.endswith("duckduckgo.com") and (path.startswith("/html") or host.startswith("html.")):
        return _duckduckgo_extraction_config(), "duckduckgo"

    # Fallback: extract from any anchors
    fallback_schema = {
        "baseSelector": "a",
        "fields": [
            {"name": "url", "type": "attribute", "attribute": "href"},
        ],
    }
    return CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema=fallback_schema)), None


async def search_urls(
    keyword: str,
    *,
    provider: str = "duckduckgo",
    site: Optional[str] = None,
    max_results: int = 20,
    browser_type: str = "chromium",
    headless: bool = True,
    lang: str = "en",
    region: str = "us",
    timebias: bool = True,
    max_paginate: Optional[int] = None,
    pagination_mode: str = "multi_window",
) -> List[str]:
    """Search a provider for URLs matching a keyword.

    Args:
        keyword: Search keyword(s).
        provider: One of "duckduckgo" (default), "google", or "pantip".
        site: Optional site restriction, e.g., "pantip.com".
        max_results: Maximum number of URLs to return.
        browser_type: Underlying browser engine for crawl4ai.
        headless: Whether to run headless.
        lang: Language code for results when supported.
        region: Region code when supported.
        timebias: When provider is "pantip", include time bias filter (newest first).
        max_paginate: When provider is "google", crawl up to this many pages (defaults to what's implied by max_results).
        pagination_mode: Either "multi_window" (default, opens separate windows for each page) or "single_window" (uses JavaScript to click next page buttons in same window).

    Returns:
        A list of cleaned absolute URLs, deduplicated and trimmed to max_results.
    """
    if max_results <= 0:
        return []

    provider = provider.lower()
    if provider not in {"duckduckgo", "google", "pantip"}:
        raise ValueError("provider must be one of: 'duckduckgo', 'google', 'pantip'")

    browser_config = BrowserConfig(browser_type=browser_type, headless=headless)

    async def _one_page(url: str, config: CrawlerRunConfig, provider_name: str) -> List[str]:
        try:
            result = await crawler.arun(url=url, config=config)
            urls: List[str] = []
            
            # Check for CAPTCHA using the reusable detector
            if result:
                is_captcha, captcha_type, details = detect_captcha(
                    url=result.url or "",
                    html_content=result.html or "",
                    domain="google.com" if provider_name == "google" else ""
                )
                
                if is_captcha:
                    # For non-headless mode, we need to handle CAPTCHA differently
                    # to keep the browser window open
                    if not headless:
                        print(f"⚠️  CAPTCHA detected: {captcha_type}")
                        print(f"   Details: {details}")
                        print(f"   URL: {url}")
                        print("   💡 Browser window is visible - solve the CAPTCHA there")
                        print("   ⏳ Waiting for CAPTCHA to be solved...")
                        print("   📝 The script will continue automatically after CAPTCHA is solved")
                        
                        # Create a new config with wait_for to detect when CAPTCHA is solved
                        # Force headless=False for CAPTCHA solving even if main script is headless
                        captcha_config = CrawlerRunConfig(
                            extraction_strategy=config.extraction_strategy,
                            js_code=config.js_code,
                            scan_full_page=config.scan_full_page,
                            magic=True,
                            simulate_user=True,
                            override_navigator=True,
                            wait_for=_get_captcha_wait_selectors(provider_name)  # Provider-specific selectors
                        )
                        
                        # Create a new browser config with headless=False for CAPTCHA solving
                        captcha_browser_config = BrowserConfig(
                            browser_type=browser_config.browser_type,
                            headless=False  # Force visible window for CAPTCHA solving
                        )
                        
                        # Wait for CAPTCHA to be solved by monitoring the page
                        max_wait_time = 300  # 5 minutes
                        wait_interval = 5    # Check every 5 seconds
                        waited_time = 0
                        
                        # Create a new crawler session with visible browser for CAPTCHA solving
                        async with AsyncWebCrawler(config=captcha_browser_config) as captcha_crawler:
                            while waited_time < max_wait_time:
                                await asyncio.sleep(wait_interval)
                                waited_time += wait_interval
                                
                                # Try to check if CAPTCHA is solved by making a request with wait_for
                                try:
                                    # Check if we can access the original search URL with wait_for
                                    check_result = await captcha_crawler.arun(url=url, config=captcha_config)
                                    if check_result and check_result.url:
                                        # Check if we're no longer on a CAPTCHA page
                                        is_still_captcha, _, _ = detect_captcha(
                                            url=check_result.url, 
                                            html_content=check_result.html or ""
                                        )
                                        if not is_still_captcha:
                                            print("   ✅ CAPTCHA appears to be solved! Continuing...")
                                            # Re-run the original search with the proper config to get results
                                            print("   🔄 Re-running search to extract results...")
                                            result = check_result #await crawler.arun(url=url, config=config)
                                            break
                                except Exception:
                                    pass
                            
                            if waited_time % 30 == 0:  # Print status every 30 seconds
                                print(f"   ⏰ Still waiting... ({waited_time}s elapsed)")
                        
                        if waited_time >= max_wait_time:
                            print("   ⚠️  Timeout waiting for CAPTCHA. Continuing anyway...")
                            # Try one more time with the original config
                            try:
                                result = await crawler.arun(url=url, config=config)
                            except Exception:
                                pass
                    else:
                        # Headless mode - use the same wait_for approach but without manual input
                        print(f"⚠️  CAPTCHA detected: {captcha_type}")
                        print(f"   Details: {details}")
                        print(f"   URL: {url}")
                        print("   ⏳ Waiting for CAPTCHA to be solved...")
                        print("   💡 Browser window will be visible for manual CAPTCHA solving")
                        
                        # Create a new config with wait_for to detect when CAPTCHA is solved
                        # Force headless=False for CAPTCHA solving even if main script is headless
                        captcha_config = CrawlerRunConfig(
                            extraction_strategy=config.extraction_strategy,
                            js_code=config.js_code,
                            scan_full_page=config.scan_full_page,
                            magic=True,
                            simulate_user=True,
                            override_navigator=True,
                            wait_for=_get_captcha_wait_selectors(provider_name)  # Provider-specific selectors
                        )
                        
                        # Create a new browser config with headless=False for CAPTCHA solving
                        captcha_browser_config = BrowserConfig(
                            browser_type=browser_config.browser_type,
                            headless=False  # Force visible window for CAPTCHA solving
                        )
                        
                        # Wait for CAPTCHA to be solved by monitoring the page
                        max_wait_time = 300  # 5 minutes - same as non-headless since we have visible window
                        wait_interval = 5    # Check every 5 seconds
                        waited_time = 0
                        
                        # Create a new crawler session with visible browser for CAPTCHA solving
                        async with AsyncWebCrawler(config=captcha_browser_config) as captcha_crawler:
                            while waited_time < max_wait_time:
                                await asyncio.sleep(wait_interval)
                                waited_time += wait_interval
                                
                                # Try to check if CAPTCHA is solved by making a request with wait_for
                                try:
                                    # Check if we can access the original search URL with wait_for
                                    check_result = await captcha_crawler.arun(url=url, config=captcha_config)
                                    if check_result and check_result.url:
                                        # Check if we're no longer on a CAPTCHA page
                                        is_still_captcha, _, _ = detect_captcha(
                                            url=check_result.url, 
                                            html_content=check_result.html or ""
                                        )
                                        if not is_still_captcha:
                                            print("   ✅ CAPTCHA appears to be solved! Continuing...")
                                            # Re-run the original search with the proper config to get results
                                            print("   🔄 Re-running search to extract results...")
                                            result = check_result
                                            break
                                except Exception:
                                    pass
                            
                            if waited_time % 15 == 0:  # Print status every 15 seconds
                                print(f"   ⏰ Still waiting... ({waited_time}s elapsed)")
                        
                        if waited_time >= max_wait_time:
                            print("   ⚠️  Timeout waiting for CAPTCHA.")
                            print("   💡 Browser window was visible for manual solving")
                            # Try one more time with the original config
                            try:
                                result = await crawler.arun(url=url, config=config)
                            except Exception:
                                pass
            
            if result and result.extracted_content:
                try:
                    items = json.loads(result.extracted_content)
                    if isinstance(items, list):
                        for item in items:
                            raw = item.get("url")
                            cleaned = _clean_search_result_url(raw, provider_name)
                            if cleaned:
                                urls.append(cleaned)
                except Exception:
                    pass
            return urls
        except Exception:
            return []

    async with AsyncWebCrawler(config=browser_config) as crawler:
        collected: List[str] = []

        if provider == "duckduckgo":
            config = _duckduckgo_extraction_config()
            per_page = 30
            pages = max(1, (max_results + per_page - 1) // per_page)
            tasks = []
            for page in range(1, pages + 1):
                url = _duckduckgo_search_url(keyword, lang=lang, region=region, page=page, site=site)
                tasks.append(asyncio.create_task(_one_page(url, config, "duckduckgo")))
            page_results = await asyncio.gather(*tasks, return_exceptions=False)
            for urls in page_results:
                collected.extend(urls)

        elif provider == "google":
            per_page = 10
            implied_pages = max(1, (max_results + per_page - 1) // per_page)
            pages = implied_pages if (max_paginate is None) else max(1, min(max_paginate, implied_pages))
            
            if pagination_mode == "single_window":
                # Single window mode: use JavaScript to paginate within one session
                config = _google_extraction_config(max_paginate=pages, pagination_mode="single_window")
                url = _google_search_url(keyword, lang=lang, region=region, start=0, site=site)
                collected.extend(await _one_page(url, config, "google"))
            else:
                # Multi-window mode: use arun_many with specialized dispatcher
                config = _google_extraction_config(max_paginate=1, pagination_mode="multi_window")
                urls_to_fetch = []
                for page in range(pages):
                    start = page * per_page
                    url = _google_search_url(keyword, lang=lang, region=region, start=start, site=site)
                    urls_to_fetch.append(url)
                
                # Create specialized Google dispatcher
                dispatcher = _create_google_dispatcher(enable_monitoring=True)
                
                # Use arun_many with dispatcher for better anti-bot handling
                async with AsyncWebCrawler(config=browser_config) as crawler:
                    try:
                        results = await crawler.arun_many(
                            urls=urls_to_fetch, 
                            config=config,
                            dispatcher=dispatcher
                        )
                    except Exception as e:
                        print(f"   ⚠️  Error in arun_many: {e}")
                        print("   🔄 Falling back to individual requests...")
                        # Fallback to individual requests
                        results = []
                        for url in urls_to_fetch:
                            try:
                                result = await crawler.arun(url=url, config=config)
                                results.append(result)
                            except Exception as url_error:
                                print(f"   ❌ Failed to fetch {url}: {url_error}")
                                results.append(None)
                    
                    for i, result in enumerate(results):
                        if result:
                            # Check for CAPTCHA
                            is_captcha, captcha_type, details = detect_captcha(
                                url=result.url or "",
                                html_content=result.html or "",
                                domain="google.com"
                            )
                            
                            if is_captcha:
                                print(f"⚠️  CAPTCHA detected on page {i + 1}: {captcha_type}")
                                print(f"   Details: {details}")
                                print(f"   URL: {urls_to_fetch[i]}")
                                print("   💡 CAPTCHA handling for multi-window mode...")
                                
                                # Handle CAPTCHA for this specific URL
                                captcha_browser_config = BrowserConfig(
                                    browser_type=browser_config.browser_type,
                                    headless=False  # Force visible window for CAPTCHA solving
                                )
                                
                                async with AsyncWebCrawler(config=captcha_browser_config) as captcha_crawler:
                                    max_wait_time = 300  # 5 minutes
                                    wait_interval = 5    # Check every 5 seconds
                                    waited_time = 0
                                    
                                    while waited_time < max_wait_time:
                                        await asyncio.sleep(wait_interval)
                                        waited_time += wait_interval
                                        
                                        try:
                                            check_result = await captcha_crawler.arun(url=urls_to_fetch[i], config=config)
                                            if check_result and check_result.url:
                                                is_still_captcha, _, _ = detect_captcha(
                                                    url=check_result.url, 
                                                    html_content=check_result.html or ""
                                                )
                                                if not is_still_captcha:
                                                    print("   ✅ CAPTCHA appears to be solved! Continuing...")
                                                    result = check_result
                                                    break
                                        except Exception:
                                            pass
                                        
                                        if waited_time % 15 == 0:
                                            print(f"   ⏰ Still waiting... ({waited_time}s elapsed)")
                                    
                                    if waited_time >= max_wait_time:
                                        print("   ⚠️  Timeout waiting for CAPTCHA. Continuing anyway...")
                        
                                        # Extract URLs from the result
                if result and result.extracted_content:
                    try:
                        page_data = json.loads(result.extracted_content)
                        page_urls = []
                        
                        for item in page_data:
                            if isinstance(item, dict) and 'url' in item:
                                cleaned_url = _clean_search_result_url(item['url'], "google")
                                if cleaned_url:
                                    page_urls.append(cleaned_url)
                        
                        collected.extend(page_urls)
                        print(f"   📄 Page {i + 1}: Found {len(page_urls)} URLs")
                        
                    except Exception as e:
                        print(f"   ❌ Error parsing page {i + 1}: {e}")
                elif result and result.html:
                    print(f"   ⚠️  Page {i + 1}: Has HTML but no extracted content")
                    # Try to extract URLs from HTML as fallback
                    try:
                        # Simple fallback extraction
                        import re
                        urls = re.findall(r'href=["\']([^"\']+)["\']', result.html)
                        for url in urls:
                            if 'google.com' not in url and url.startswith('http'):
                                cleaned_url = _clean_search_result_url(url, "google")
                                if cleaned_url:
                                    collected.append(cleaned_url)
                        print(f"   📄 Page {i + 1}: Found {len(urls)} URLs from HTML fallback")
                    except Exception as fallback_error:
                        print(f"   ❌ Fallback extraction failed for page {i + 1}: {fallback_error}")
                else:
                    print(f"   ⚠️  Page {i + 1}: No content extracted")

        elif provider == "pantip":
            config = _pantip_extraction_config()
            url = _pantip_search_url(keyword, timebias=timebias)
            collected.extend(await _one_page(url, config, "pantip"))

        cleaned_unique = _unique_preserve_order(collected)
        return cleaned_unique[:max_results]


# Convenience helpers for common scenarios
async def search_google(keyword: str, *, max_results: int = 20, site: Optional[str] = None, pagination_mode: str = "multi_window", **kwargs) -> List[str]:
    return await search_urls(keyword, provider="google", max_results=max_results, site=site, pagination_mode=pagination_mode, **kwargs)


async def search_duckduckgo(keyword: str, *, max_results: int = 20, site: Optional[str] = None, **kwargs) -> List[str]:
    return await search_urls(keyword, provider="duckduckgo", max_results=max_results, site=site, **kwargs)


async def search_pantip(keyword: str, *, max_results: int = 20, timebias: bool = True, **kwargs) -> List[str]:
    return await search_urls(keyword, provider="pantip", max_results=max_results, timebias=timebias, **kwargs)


async def search_from_url(
    search_url: str,
    extraction_schema: Optional[Dict] = None,
    *,
    provider: Optional[str] = None,
    browser_type: str = "chromium",
    headless: bool = True,
    max_results: Optional[int] = None,
    return_schema: bool = True,
    max_paginate: Optional[int] = None,
    pagination_mode: str = "multi_window",
) -> Union[List[Dict[str, Any]], List[str]]:
    """Generic search: pass a search URL; config is inferred from base URL unless a schema is provided.

    Args:
        search_url: The full search results URL to fetch.
        extraction_schema: Optional JsonCssExtractionStrategy schema with fields including 'url'. If None, infer from base URL.
        provider: Optional provider hint for URL cleaning (e.g., 'google', 'duckduckgo', 'pantip'). If None, inferred.
        browser_type: Browser engine for crawl4ai.
        headless: Run browser headless.
        max_results: If provided, limit the number of items returned.
        return_schema: When True (default), return full JSON-like records per schema; when False, return a list of URLs only.

    Returns:
        A list of dicts as extracted by the schema (JSON-like). The 'url' field is cleaned/normalized when possible.
    """
    browser_config = BrowserConfig(browser_type=browser_type, headless=headless)
    if extraction_schema is None:
        run_config, inferred_provider = _extraction_config_for_url(search_url)
        # If Google auto-config is used, disable auto-next to allow explicit pagination
        inferred_host = (urlparse(search_url).hostname or "").lower()
        if inferred_host and "google." in inferred_host and isinstance(max_paginate, int):
            run_config = _google_extraction_config(max_paginate=1, pagination_mode=pagination_mode)
        provider = provider or inferred_provider
    else:
        run_config = CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema=extraction_schema))

    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            # Collect results potentially across pages
            records: List[Dict[str, Any]] = []
            urls_to_fetch: List[str] = [search_url]

            # If Google, compute paginated URLs explicitly
            if provider == "google":
                per_page = 10
                if max_paginate is None:
                    # If max_results is set, infer pages; else default to 1
                    implied_pages = 1 if not max_results else max(1, (max_results + per_page - 1) // per_page)
                    pages = implied_pages
                else:
                    pages = max(1, int(max_paginate))
                
                if pagination_mode == "single_window":
                    # Single window mode: use JavaScript pagination, start from first page
                    if search_url.find("&start=") == -1 and search_url.find("?start=") == -1:
                        # Use the base URL and let JavaScript handle pagination
                        urls_to_fetch = [search_url]
                        # Update the config to use JavaScript pagination
                        run_config = _google_extraction_config(max_paginate=pages, pagination_mode="single_window")
                    else:
                        # If start parameter exists, extract base URL and use JavaScript pagination
                        base_url = search_url.split("&start=")[0].split("?start=")[0]
                        urls_to_fetch = [base_url]
                        run_config = _google_extraction_config(max_paginate=pages, pagination_mode="single_window")
                else:
                    # Multi-window mode: build explicit page URLs
                    if search_url.find("&start=") == -1 and search_url.find("?start=") == -1:
                        # Build explicit page URLs from base query
                        parsed = urlparse(search_url)
                        # We cannot easily recompose query safely here without parsing; reuse helper by extracting q/gl/hl if desired.
                        # Fallback: append start param for pages > 0
                        base = search_url
                        urls_to_fetch = []
                        for page in range(pages):
                            start = page * per_page
                            if "?" in base:
                                urls_to_fetch.append(f"{base}&start={start}")
                            else:
                                urls_to_fetch.append(f"{base}?start={start}")
                    else:
                        # If 'start' exists already, assume caller provided full pagination; fetch as-is only
                        urls_to_fetch = [search_url]

            # Fetch pages and aggregate using arun_many with dispatcher
            if provider == "google":
                # Use specialized Google dispatcher
                dispatcher = _create_google_dispatcher(enable_monitoring=True)
                try:
                    results = await crawler.arun_many(
                        urls=urls_to_fetch, 
                        config=run_config,
                        dispatcher=dispatcher
                    )
                except Exception as e:
                    print(f"   ⚠️  Error in arun_many: {e}")
                    print("   🔄 Falling back to individual requests...")
                    # Fallback to individual requests
                    results = []
                    for url in urls_to_fetch:
                        try:
                            result = await crawler.arun(url=url, config=run_config)
                            results.append(result)
                        except Exception as url_error:
                            print(f"   ❌ Failed to fetch {url}: {url_error}")
                            results.append(None)
            else:
                # Use default dispatcher for other providers
                try:
                    results = await crawler.arun_many(urls=urls_to_fetch, config=run_config)
                except Exception as e:
                    print(f"   ⚠️  Error in arun_many: {e}")
                    print("   🔄 Falling back to individual requests...")
                    # Fallback to individual requests
                    results = []
                    for url in urls_to_fetch:
                        try:
                            result = await crawler.arun(url=url, config=run_config)
                            results.append(result)
                        except Exception as url_error:
                            print(f"   ❌ Failed to fetch {url}: {url_error}")
                            results.append(None)
            
            for i, res in enumerate(results):
                if res:
                    # Check for CAPTCHA
                    is_captcha, captcha_type, details = detect_captcha(
                        url=res.url or "",
                        html_content=res.html or "",
                        domain="google.com" if provider == "google" else ""
                    )
                    
                    if is_captcha:
                        print(f"⚠️  CAPTCHA detected on page {i + 1}: {captcha_type}")
                        print(f"   Details: {details}")
                        print(f"   URL: {urls_to_fetch[i]}")
                        print("   💡 CAPTCHA handling for multi-window mode...")
                        
                        # Handle CAPTCHA for this specific URL
                        captcha_browser_config = BrowserConfig(
                            browser_type=browser_config.browser_type,
                            headless=False  # Force visible window for CAPTCHA solving
                        )
                        
                        async with AsyncWebCrawler(config=captcha_browser_config) as captcha_crawler:
                            max_wait_time = 300  # 5 minutes
                            wait_interval = 5    # Check every 5 seconds
                            waited_time = 0
                            
                            while waited_time < max_wait_time:
                                await asyncio.sleep(wait_interval)
                                waited_time += wait_interval
                                
                                try:
                                    check_result = await captcha_crawler.arun(url=urls_to_fetch[i], config=run_config)
                                    if check_result and check_result.url:
                                        is_still_captcha, _, _ = detect_captcha(
                                            url=check_result.url, 
                                            html_content=check_result.html or ""
                                        )
                                        if not is_still_captcha:
                                            print("   ✅ CAPTCHA appears to be solved! Continuing...")
                                            res = check_result
                                            break
                                except Exception:
                                    pass
                                
                                if waited_time % 15 == 0:
                                    print(f"   ⏰ Still waiting... ({waited_time}s elapsed)")
                            
                            if waited_time >= max_wait_time:
                                print("   ⚠️  Timeout waiting for CAPTCHA. Continuing anyway...")
                
                # Extract records from the result
                if res and res.extracted_content:
                    try:
                        items = json.loads(res.extracted_content)
                        if isinstance(items, list):
                            for item in items:
                                if not isinstance(item, dict):
                                    continue
                                record = dict(item)
                                raw = record.get("url")
                                if provider:
                                    cleaned = _clean_search_result_url(raw, provider)
                                    if not cleaned:
                                        continue
                                    record["url"] = cleaned
                                records.append(record)
                    except Exception as e:
                        print(f"   ❌ Error parsing page {i + 1}: {e}")
            # Deduplicate by URL preserving order
            if return_schema:
                seen: set = set()
                deduped: List[Dict[str, Any]] = []
                for rec in records:
                    url_val = rec.get("url")
                    if not url_val or url_val in seen:
                        continue
                    seen.add(url_val)
                    deduped.append(rec)
                if max_results is not None and max_results >= 0:
                    deduped = deduped[:max_results]
                return deduped
            else:
                urls_only: List[str] = []
                for rec in records:
                    u = rec.get("url")
                    if isinstance(u, str):
                        urls_only.append(u)
                urls_only = _unique_preserve_order(urls_only)
                if max_results is not None and max_results >= 0:
                    urls_only = urls_only[:max_results]
                return urls_only
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []


async def search_keywords_all_platforms(
    keywords: List[str],
    *,
    providers: Optional[List[str]] = None,
    max_results_per_provider: int = 10,
    timebias: bool = True,
    max_concurrent: int = 3,
) -> List[Dict[str, str]]:
    """Search multiple keywords across all supported providers and return URL-platform pairs.

    Args:
        keywords: List of keywords to search.
        providers: Optional subset of providers to use. Defaults to ["pantip", "google", "duckduckgo"].
        max_results_per_provider: Max URLs to fetch per (keyword, provider) pair.
        timebias: Passed to Pantip search to bias towards recent.
        max_concurrent: Limit on concurrent searches to avoid spawning too many browsers.

    Returns:
        List of dicts: [{"url": "...", "platform": "pantip"}, ...], deduplicated by URL preserving order.
    """
    if not keywords:
        return []

    all_providers = ["pantip", "google", "duckduckgo"]
    if providers:
        providers = [p.lower() for p in providers if p.lower() in all_providers]
    used_providers = providers or all_providers

    semaphore = asyncio.Semaphore(max(1, max_concurrent))

    async def _run_one(keyword: str, provider: str) -> List[Dict[str, str]]:
        async with semaphore:
            try:
                if provider == "pantip":
                    urls = await search_pantip(keyword, max_results=max_results_per_provider, timebias=timebias)
                elif provider == "google":
                    urls = await search_google(keyword, max_results=max_results_per_provider)
                elif provider == "duckduckgo":
                    urls = await search_duckduckgo(keyword, max_results=max_results_per_provider)
                else:
                    return []
                return [{"url": u, "platform": provider} for u in urls]
            except Exception as e:
                # If it's a Google search and we get an exception, it might be CAPTCHA-related
                if provider == "google":
                    print(f"⚠️  Error during Google search for '{keyword}': {str(e)}")
                    print("   This might be due to CAPTCHA. Consider waiting before retrying.")
                return []

    tasks: List[asyncio.Task] = []
    for kw in keywords:
        for prov in used_providers:
            tasks.append(asyncio.create_task(_run_one(kw, prov)))

    results_grouped = await asyncio.gather(*tasks, return_exceptions=False)

    # Deduplicate by URL while preserving first-found platform and order
    seen: set = set()
    combined: List[Dict[str, str]] = []
    for group in results_grouped:
        for item in group:
            url = item.get("url")
            if not url or url in seen:
                continue
            seen.add(url)
            combined.append({"url": url, "platform": item.get("platform", "")})

    return combined



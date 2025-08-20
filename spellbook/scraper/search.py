import asyncio
import json
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode, urlparse, parse_qs, unquote

from crawl4ai import AsyncWebCrawler
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, VirtualScrollConfig


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


def _google_extraction_config(max_paginate: int = 3) -> CrawlerRunConfig:
    # Organic results are usually wrapped in .g under #search
    schema = {
        "baseSelector": "#rso > div[class='MjjYud']", #"#search .g",
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

    # JS code to paginate
    js_code = f"""
    async function paginate() {{
        let maxPages = {max_paginate};
        for (let i = 0; i < maxPages - 1; i++) {{
            let nextBtn = document.querySelector("a#pnnext");
            if (!nextBtn) break;
            nextBtn.click();
            await new Promise(r => setTimeout(r, 2000)); // wait for next page load
        }}
    }}
    await paginate();
    """

    return CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema=schema),
                            js_code=js_code,
                            scan_full_page=True)


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
        scroll_count=100,                    # Number of scrolls to perform
        scroll_by="container_height",       # How much to scroll each time
        wait_after_scroll=0.5               # Wait time (seconds) after each scroll
    )
    return CrawlerRunConfig(extraction_strategy=JsonCssExtractionStrategy(schema=schema), 
                            virtual_scroll_config=virtual_config,
                            scan_full_page=True,
                            scroll_delay=0.5,)


from typing import Tuple


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
            # Disable auto-pagination js; we page explicitly
            config = _google_extraction_config(max_paginate=1)
            per_page = 10
            implied_pages = max(1, (max_results + per_page - 1) // per_page)
            pages = implied_pages if (max_paginate is None) else max(1, min(max_paginate, implied_pages))
            tasks = []
            for page in range(pages):
                start = page * per_page
                url = _google_search_url(keyword, lang=lang, region=region, start=start, site=site)
                tasks.append(asyncio.create_task(_one_page(url, config, "google")))
            page_results = await asyncio.gather(*tasks, return_exceptions=False)
            for urls in page_results:
                collected.extend(urls)

        elif provider == "pantip":
            config = _pantip_extraction_config()
            url = _pantip_search_url(keyword, timebias=timebias)
            collected.extend(await _one_page(url, config, "pantip"))

        cleaned_unique = _unique_preserve_order(collected)
        return cleaned_unique[:max_results]


# Convenience helpers for common scenarios
async def search_google(keyword: str, *, max_results: int = 20, site: Optional[str] = None, **kwargs) -> List[str]:
    return await search_urls(keyword, provider="google", max_results=max_results, site=site, **kwargs)


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
            run_config = _google_extraction_config(max_paginate=1)
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

            # Fetch pages and aggregate
            async def _fetch_one(u: str) -> List[Dict[str, Any]]:
                try:
                    res = await crawler.arun(url=u, config=run_config)
                    page_records: List[Dict[str, Any]] = []
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
                                    page_records.append(record)
                        except Exception:
                            pass
                    return page_records
                except Exception:
                    return []

            page_tasks = [asyncio.create_task(_fetch_one(u)) for u in urls_to_fetch]
            page_results = await asyncio.gather(*page_tasks, return_exceptions=False)
            for group in page_results:
                records.extend(group)
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
        except Exception:
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
            except Exception:
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



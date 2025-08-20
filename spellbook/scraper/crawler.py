#import httpx
import asyncio
import json
from typing import Dict, List, Optional
from urllib.parse import urlparse

from crawl4ai import AsyncWebCrawler
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from pprint import pprint

# ------------------------------------------------------------
# Domain-aware schemas with a consistent output contract
# Required fields across all schemas: id, title, content, date
# ------------------------------------------------------------

def _normalize_domain(hostname: str) -> str:
    """Return the registrable domain key used for schema lookup."""
    if not hostname:
        return ""
    hostname = hostname.lower()
    # Strip common subdomains
    for prefix in ("www.", "m."):
        if hostname.startswith(prefix):
            hostname = hostname[len(prefix):]
    return hostname


def _schema_for_domain(domain: str) -> Dict:
    """Return a JsonCssExtractionStrategy schema for the given domain.

    The schema MUST provide these fields: id, title, content, date.
    """
    # Pantip topic page (single main post)
    if domain.endswith("pantip.com"):
        return {
            "baseSelector": ".display-post-wrapper.main-post.type",
            "fields": [
                {"name": "id", "type": "attribute", "attribute": "id"},
                {"name": "title", "selector": "h1.display-post-title", "type": "text"},
                {"name": "content", "selector": "div.display-post-story", "type": "text"},
                {"name": "date", "selector": "abbr.timeago", "type": "attribute", "attribute": "data-utime"},
            ],
        }

    # X/Twitter single-tweet page
    if domain.endswith("x.com") or domain.endswith("twitter.com"):
        return {
            "baseSelector": "article[data-testid='tweet']",
            "fields": [
                # Full tweet URL (id embedded inside). Using href keeps things robust across DOM changes
                {"name": "id", "selector": "a[href*='/status/']", "type": "attribute", "attribute": "href"},
                # Use display name as a stable title surrogate for tweets
                {"name": "title", "selector": "div[data-testid='User-Name'] span", "type": "text"},
                {"name": "content", "selector": "div[data-testid='tweetText']", "type": "text"},
                {"name": "date", "selector": "time[datetime]", "type": "attribute", "attribute": "datetime"},
            ],
        }

    # Generic fallback using common metadata and structures
    # Note: We scope from html so selectors can target head metadata as well
    return {
        "baseSelector": "html",
        "fields": [
            {"name": "id", "selector": "link[rel='canonical']", "type": "attribute", "attribute": "href"},
            {"name": "title", "selector": "meta[property='og:title']", "type": "attribute", "attribute": "content"},
            {"name": "content", "selector": "article", "type": "text"},
            {"name": "date", "selector": "meta[property='article:published_time']", "type": "attribute", "attribute": "content"},
        ],
    }


def _build_config_for_url(url: str) -> CrawlerRunConfig:
    domain = _normalize_domain(urlparse(url).hostname or "")
    schema = _schema_for_domain(domain)
    return CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(schema=schema)
    )


async def crawl(urls: List[str], *, browser_type: str = "chromium", headless: bool = True) -> List[Dict[str, Optional[str]]]:
    """Crawl a list of URLs using domain-specific schemas.

    Ensures consistent fields across outputs: id, title, content, date.

    Args:
        urls: List of page URLs to crawl.
        browser_type: Browser engine for the underlying crawler.
        headless: Whether to run the browser in headless mode.

    Returns:
        A list where each item corresponds to a URL, containing
        at least keys: id, title, content, date. Missing values are None.
    """
    if not urls:
        return []

    browser_config = BrowserConfig(browser_type=browser_type, headless=headless)
    async def _crawl_one(crawler: AsyncWebCrawler, url: str) -> Dict[str, Optional[str]]:
        try:
            config = _build_config_for_url(url)
            result = await crawler.arun(url=url, config=config)

            record: Dict[str, Optional[str]] = {"id": None, "title": None, "content": None, "date": None}

            if result and result.extracted_content:
                try:
                    extracted = json.loads(result.extracted_content)
                    if isinstance(extracted, list) and extracted:
                        first = extracted[0]
                        record["id"] = first.get("id")
                        record["title"] = first.get("title")
                        record["content"] = first.get("content")
                        record["date"] = first.get("date")
                except Exception:
                    pass

            return record
        except Exception:
            return {"id": None, "title": None, "content": None, "date": None}

    async with AsyncWebCrawler(config=browser_config) as crawler:
        tasks = [asyncio.create_task(_crawl_one(crawler, u)) for u in urls]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return list(results)


'''async def crawl():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11235/crawl",
            json={
                "urls": [
                    "https://pantip.com/topic/43693765"
                ],
                "crawler_config": {
                    "type": "CrawlerRunConfig",
                    "params": {
                        "scraping_strategy": {
                            "type": "LXMLWebScrapingStrategy", #"MarkdownWebScrapingStrategy",
                            "params": {},
                            "schema": {
                                "bobo": {
                                    "css_selector": "div.display-post-story-footer abbr.timeago",
                                    "attribute": "data-utime"
                                },
                            }                     
                        },
                        "table_extraction": {
                            "type": "DefaultTableExtraction",
                            "params": {}
                        },
                        "exclude_social_media_domains": [
                            "facebook.com",
                            "twitter.com",
                            "x.com",
                            "linkedin.com",
                            "instagram.com",
                            "pinterest.com",
                            "tiktok.com",
                            "snapchat.com",
                            "reddit.com"
                        ],
                        "stream": True,
                    }
                }
            }
        )
        return response.json()'''
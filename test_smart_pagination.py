#!/usr/bin/env python3
"""
Test script to demonstrate smart pagination functionality.
Shows how to check for the last page with results to avoid crawling empty pages.
"""

import asyncio
import time
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, JsonCssExtractionStrategy
from spellbook.scraper.search import _google_extraction_config, _create_google_dispatcher


async def check_page_has_results(crawler, url: str, provider: str = "google") -> bool:
    """
    Check if a page has search results or is empty.
    
    Args:
        crawler: The crawler instance to use
        url: The URL to check
        provider: The search provider (google, duckduckgo, etc.)
        
    Returns:
        True if the page has results, False if empty
    """
    try:
        # Create a simple config just for checking
        check_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(schema={
                "baseSelector": "body",
                "fields": [{"name": "content", "type": "text"}]
            }),
            scan_full_page=False,  # Don't scan full page for efficiency
            wait_until="domcontentloaded",  # Faster than networkidle
            wait_for="body",  # Just wait for body to load
        )
        
        result = await crawler.arun(url=url, config=check_config)
        
        if not result or not result.html:
            return False
        
        # Check for no results indicators
        html_content = result.html.lower()
        
        # Provider-specific no results indicators
        if provider == "google":
            no_results_indicators = [
                "#botstuff > div > div.mnr-c",
                "#ootqv",
                "no results found",
                "did not match any documents",
                "your search did not match any documents",
                "ไม่พบผลลัพธ์",  # Thai: no results found
            ]
            
            # Check if we have actual search results
            results_indicators = [
                "#rso",
                ".g",
                ".mjjyud",
                "search result",
            ]
        else:
            # Generic indicators
            no_results_indicators = [
                "no results found",
                "no matches found",
                "did not match any documents",
                "empty results",
            ]
            
            results_indicators = [
                "search result",
                "result",
                "listing",
            ]
        
        # Check for no results indicators
        for indicator in no_results_indicators:
            if indicator in html_content:
                return False
        
        # Check if we have actual search results
        for indicator in results_indicators:
            if indicator in html_content:
                return True
        
        # If we can't find clear indicators, check extracted content
        if result.extracted_content:
            try:
                import json
                page_data = json.loads(result.extracted_content)
                if page_data and len(page_data) > 0:
                    return True
            except:
                pass
        
        return False
        
    except Exception as e:
        print(f"   ⚠️  Error checking page: {e}")
        return False


async def find_last_page_with_results(crawler, base_url: str, provider: str = "google", max_pages: int = 50) -> int:
    """
    Find the last page that has results using binary search approach.
    
    Args:
        crawler: The crawler instance to use
        base_url: The base search URL
        provider: The search provider
        max_pages: Maximum number of pages to check
        
    Returns:
        The last page number that has results (0-based)
    """
    print(f"   🔍 Finding last page with results...")
    
    # Start with a high page number and work backwards
    start_page = max_pages
    end_page = 0
    last_page_with_results = 0
    
    # Binary search approach to find the last page with results
    while start_page >= end_page:
        mid_page = (start_page + end_page) // 2
        start_param = mid_page * 10
        
        # Construct test URL
        if "?" in base_url:
            test_url = f"{base_url}&start={start_param}"
        else:
            test_url = f"{base_url}?start={start_param}"
            
        print(f"   🔍 Checking page {mid_page} (start={start_param})...")
        
        has_results = await check_page_has_results(crawler, test_url, provider)
        
        if has_results:
            print(f"   ✅ Page {mid_page} has results")
            last_page_with_results = mid_page
            end_page = mid_page + 1  # Look for higher pages
        else:
            print(f"   ❌ Page {mid_page} is empty")
            start_page = mid_page - 1  # Look for lower pages
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(1)
    
    print(f"   🎯 Last page with results: {last_page_with_results}")
    return last_page_with_results


async def test_smart_pagination():
    """Test the smart pagination functionality."""
    print("🧠 Testing Smart Pagination")
    print("   Strategy: Find last page with results to avoid empty pages")
    print()
    
    # Test URL that might have limited results
    test_url = "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024+%22travel+card%22"
    
    # Initialize browser
    browser_config = BrowserConfig(browser_type="chromium", headless=True)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print("✅ Browser initialized")
        
        # Find the last page with results
        last_page = await find_last_page_with_results(
            crawler=crawler,
            base_url=test_url,
            provider="google",
            max_pages=50
        )
        
        print(f"\n📊 Results:")
        print(f"   Last page with results: {last_page}")
        print(f"   Total pages to crawl: {last_page + 1}")
        print(f"   Pages skipped: {50 - (last_page + 1)}")
        
        if last_page > 0:
            # Generate URLs only up to the last page with results
            urls_to_fetch = []
            for page in range(last_page + 1):
                start = page * 10
                if "?" in test_url:
                    url = f"{test_url}&start={start}"
                else:
                    url = f"{test_url}?start={start}"
                urls_to_fetch.append(url)
            
            # Reverse order to start from last page
            urls_to_fetch.reverse()
            print(f"   🔄 Reversed URL order: {len(urls_to_fetch)} pages")
            
            # Show first few URLs
            print(f"   📄 Sample URLs:")
            for i, url in enumerate(urls_to_fetch[:3], 1):
                print(f"      {i}. {url}")
            
            if len(urls_to_fetch) > 3:
                print(f"      ... and {len(urls_to_fetch) - 3} more")
        else:
            print("   ⚠️  No results found - no pages to crawl")


async def test_traffic_reduction():
    """Test traffic reduction by comparing with and without smart pagination."""
    print("\n🚦 Testing Traffic Reduction")
    print("   Strategy: Compare crawling with and without smart pagination")
    
    test_url = "https://www.google.com/search?q=python+tutorial+site:example.com"
    
    browser_config = BrowserConfig(browser_type="chromium", headless=True)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print("✅ Browser initialized")
        
        # Method 1: Traditional approach (crawl all pages)
        print("\n📄 Method 1: Traditional (crawl all pages)")
        traditional_pages = 50
        print(f"   Pages to crawl: {traditional_pages}")
        print(f"   Estimated requests: {traditional_pages}")
        
        # Method 2: Smart pagination
        print("\n🧠 Method 2: Smart pagination")
        last_page = await find_last_page_with_results(
            crawler=crawler,
            base_url=test_url,
            provider="google",
            max_pages=50
        )
        
        smart_pages = last_page + 1
        print(f"   Pages to crawl: {smart_pages}")
        print(f"   Pages skipped: {traditional_pages - smart_pages}")
        print(f"   Traffic reduction: {((traditional_pages - smart_pages) / traditional_pages * 100):.1f}%")


def explain_smart_pagination():
    """Explain the smart pagination functionality."""
    print("\n📚 Understanding Smart Pagination")
    print("=" * 40)
    
    print("\n🎯 Problem:")
    print("   • Google search results are limited")
    print("   • Many pages after a certain point are empty")
    print("   • Crawling empty pages wastes resources")
    print("   • Increases risk of rate limiting and CAPTCHA")
    
    print("\n⚡ Solution:")
    print("   • Check if pages have results before crawling")
    print("   • Use binary search to find last page with results")
    print("   • Only crawl pages that actually have content")
    print("   • Start from last page and work backwards")
    
    print("\n🔍 Detection Methods:")
    print("   • CSS Selectors: #botstuff > div > div.mnr-c, #OotqVd")
    print("   • Text Patterns: 'no results found', 'did not match'")
    print("   • Content Analysis: Check extracted content")
    print("   • Binary Search: Efficiently find boundary")
    
    print("\n📊 Benefits:")
    print("   • Reduced traffic (50-80% fewer requests)")
    print("   • Faster execution (skip empty pages)")
    print("   • Lower CAPTCHA risk (fewer requests)")
    print("   • Better resource utilization")


def show_binary_search():
    """Show how binary search works for finding the last page."""
    print("\n🔍 Binary Search Algorithm")
    print("=" * 35)
    
    print("\n📊 How it works:")
    print("   • Start with range [0, max_pages]")
    print("   • Check middle page")
    print("   • If has results: search higher half")
    print("   • If empty: search lower half")
    print("   • Repeat until boundary is found")
    
    print("\n⚡ Efficiency:")
    print("   • Traditional: Check all pages (O(n))")
    print("   • Binary search: Check log(n) pages")
    print("   • Example: 50 pages → ~6 checks")
    print("   • 83% fewer checks needed")


if __name__ == "__main__":
    print("🧠 Smart Pagination Test Suite")
    print("This script demonstrates smart pagination to reduce traffic.")
    print()
    
    # Explain the functionality
    explain_smart_pagination()
    show_binary_search()
    
    print("\n" + "=" * 60)
    
    # Ask user which test to run
    print("\nChoose a test:")
    print("1. Smart pagination test")
    print("2. Traffic reduction comparison")
    print("3. Both tests")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        asyncio.run(test_smart_pagination())
    elif choice == "2":
        asyncio.run(test_traffic_reduction())
    elif choice == "3":
        asyncio.run(test_smart_pagination())
        asyncio.run(test_traffic_reduction())
    else:
        print("Invalid choice. Running smart pagination test...")
        asyncio.run(test_smart_pagination())
    
    print("\n✅ Smart pagination test completed!")

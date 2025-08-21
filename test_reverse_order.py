#!/usr/bin/env python3
"""
Test script to demonstrate the reverse order functionality.
Shows how URLs are processed starting from the last page (backward) vs first page (forward).
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_reverse_order():
    """Test the reverse order functionality."""
    print("🔄 Testing Reverse Order Functionality")
    print("   Strategy: Start from last page and work backwards")
    print()
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "python tutorial",
            max_results=15,
            max_paginate=3,
            pagination_mode="multi_window",
            reverse_order=True,  # Start from last page
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Reverse order completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ Reverse order failed: {e}")


async def test_forward_order():
    """Test the forward order functionality."""
    print("\n📄 Testing Forward Order Functionality")
    print("   Strategy: Start from first page and work forwards")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "python tutorial",
            max_results=15,
            max_paginate=3,
            pagination_mode="multi_window",
            reverse_order=False,  # Start from first page
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Forward order completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Forward order failed: {e}")


async def test_single_window_reverse():
    """Test reverse order with single window pagination."""
    print("\n🪟 Testing Single Window Reverse Order...")
    print("   Strategy: JavaScript pagination with reverse order")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "machine learning tutorial",
            max_results=20,
            max_paginate=2,
            pagination_mode="single_window",
            reverse_order=True,  # Start from last page
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Single window reverse order completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Single window reverse order failed: {e}")


async def test_search_from_url_reverse():
    """Test reverse order with search_from_url function."""
    print("\n🔗 Testing search_from_url Reverse Order...")
    print("   Strategy: Direct URL with reverse order pagination")
    
    start_time = time.time()
    
    try:
        # Test with a Google search URL
        search_url = "https://www.google.com/search?q=python+tutorial&hl=en&gl=us"
        results = await search_from_url(
            search_url,
            max_results=15,
            max_paginate=3,
            pagination_mode="multi_window",
            reverse_order=True,  # Start from last page
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ search_from_url reverse order completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        if isinstance(results, list) and len(results) > 0:
            if isinstance(results[0], dict):
                # Full schema results
                for i, result in enumerate(results[:3], 1):
                    url = result.get('url', 'No URL')
                    title = result.get('title', 'No title')
                    print(f"   {i}. {title}")
                    print(f"      URL: {url}")
            else:
                # URL-only results
                for i, url in enumerate(results[:3], 1):
                    print(f"   {i}. {url}")
        
    except Exception as e:
        print(f"❌ search_from_url reverse order failed: {e}")


async def test_search_from_url_forward():
    """Test forward order with search_from_url function."""
    print("\n🔗 Testing search_from_url Forward Order...")
    print("   Strategy: Direct URL with forward order pagination")
    
    start_time = time.time()
    
    try:
        # Test with a Google search URL
        search_url = "https://www.google.com/search?q=machine+learning&hl=en&gl=us"
        results = await search_from_url(
            search_url,
            max_results=15,
            max_paginate=3,
            pagination_mode="multi_window",
            reverse_order=False,  # Start from first page
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ search_from_url forward order completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ search_from_url forward order failed: {e}")


def explain_reverse_order():
    """Explain the reverse order functionality."""
    print("\n📚 Understanding Reverse Order")
    print("=" * 35)
    
    print("\n🎯 Purpose:")
    print("   • Start crawling from the last page")
    print("   • Work backwards through search results")
    print("   • Useful for getting most recent results first")
    print("   • Helps with rate limiting and CAPTCHA avoidance")
    
    print("\n🔄 How It Works:")
    print("   • Generate URLs for all pages (page 1, 2, 3, ...)")
    print("   • Reverse the list (page 3, 2, 1, ...)")
    print("   • Process URLs in reverse order")
    print("   • Results are still returned in chronological order")
    
    print("\n📊 Benefits:")
    print("   • Get latest results first")
    print("   • Better for time-sensitive searches")
    print("   • May avoid early CAPTCHA triggers")
    print("   • More efficient for recent content")
    
    print("\n⚙️ Configuration:")
    print("   • reverse_order=True (default): Start from last page")
    print("   • reverse_order=False: Start from first page")
    print("   • Works with both multi_window and single_window modes")


def show_url_generation():
    """Show how URLs are generated and reversed."""
    print("\n🔗 URL Generation and Reversal")
    print("=" * 40)
    
    print("\n📄 Forward Order (reverse_order=False):")
    print("   Page 1: https://google.com/search?q=test&start=0")
    print("   Page 2: https://google.com/search?q=test&start=10")
    print("   Page 3: https://google.com/search?q=test&start=20")
    print("   Processing order: 1 → 2 → 3")
    
    print("\n🔄 Reverse Order (reverse_order=True):")
    print("   Page 1: https://google.com/search?q=test&start=0")
    print("   Page 2: https://google.com/search?q=test&start=10")
    print("   Page 3: https://google.com/search?q=test&start=20")
    print("   After reversal: 3 → 2 → 1")
    print("   Processing order: 3 → 2 → 1")
    
    print("\n📊 Result Order:")
    print("   • URLs are processed in reverse order")
    print("   • Results are still returned chronologically")
    print("   • Latest content appears first in results")


def compare_approaches():
    """Compare forward vs reverse order approaches."""
    print("\n🔄 Order Approach Comparison")
    print("=" * 35)
    
    approaches = [
        {
            "name": "📄 Forward Order (reverse_order=False)",
            "description": "Start from page 1 and work forwards",
            "pros": ["Traditional approach", "Predictable order", "Good for historical data"],
            "cons": ["May hit rate limits early", "Older content first", "Less efficient for recent data"]
        },
        {
            "name": "🔄 Reverse Order (reverse_order=True)",
            "description": "Start from last page and work backwards",
            "pros": ["Latest content first", "May avoid early CAPTCHA", "Better for recent data"],
            "cons": ["Less predictable", "May miss early pages if interrupted", "Different user experience"]
        }
    ]
    
    for i, approach in enumerate(approaches, 1):
        print(f"\n{i}. {approach['name']}")
        print(f"   {approach['description']}")
        print("   Pros:")
        for pro in approach['pros']:
            print(f"      • {pro}")
        print("   Cons:")
        for con in approach['cons']:
            print(f"      • {con}")


def show_use_cases():
    """Show different use cases for reverse order."""
    print("\n🎯 Use Cases for Reverse Order")
    print("=" * 35)
    
    use_cases = [
        {
            "scenario": "Recent News Search",
            "description": "Looking for latest news articles",
            "benefit": "Get most recent news first",
            "recommendation": "Use reverse_order=True"
        },
        {
            "scenario": "Historical Research",
            "description": "Looking for older, established content",
            "benefit": "Get comprehensive historical coverage",
            "recommendation": "Use reverse_order=False"
        },
        {
            "scenario": "CAPTCHA Avoidance",
            "description": "Trying to avoid early CAPTCHA triggers",
            "benefit": "May avoid rate limiting on early pages",
            "recommendation": "Use reverse_order=True"
        },
        {
            "scenario": "Time-Sensitive Content",
            "description": "Looking for recent updates or changes",
            "benefit": "Get latest versions of content",
            "recommendation": "Use reverse_order=True"
        }
    ]
    
    for i, case in enumerate(use_cases, 1):
        print(f"\n{i}. {case['scenario']}")
        print(f"   {case['description']}")
        print(f"   Benefit: {case['benefit']}")
        print(f"   Recommendation: {case['recommendation']}")


if __name__ == "__main__":
    print("🔄 Reverse Order Test Suite")
    print("This script demonstrates URL list reversal functionality.")
    print()
    
    # Explain the functionality
    explain_reverse_order()
    show_url_generation()
    compare_approaches()
    show_use_cases()
    
    print("\n" + "=" * 60)
    
    # Ask user which test to run
    print("\nChoose a test:")
    print("1. Reverse order test (start from last page)")
    print("2. Forward order test (start from first page)")
    print("3. Single window reverse order test")
    print("4. search_from_url reverse order test")
    print("5. search_from_url forward order test")
    print("6. All tests")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        asyncio.run(test_reverse_order())
    elif choice == "2":
        asyncio.run(test_forward_order())
    elif choice == "3":
        asyncio.run(test_single_window_reverse())
    elif choice == "4":
        asyncio.run(test_search_from_url_reverse())
    elif choice == "5":
        asyncio.run(test_search_from_url_forward())
    elif choice == "6":
        asyncio.run(test_reverse_order())
        asyncio.run(test_forward_order())
        asyncio.run(test_single_window_reverse())
        asyncio.run(test_search_from_url_reverse())
        asyncio.run(test_search_from_url_forward())
    else:
        print("Invalid choice. Running reverse order test...")
        asyncio.run(test_reverse_order())

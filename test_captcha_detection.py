#!/usr/bin/env python3
"""
Test script to demonstrate CAPTCHA detection in Google search functionality.
"""

import asyncio
from spellbook.scraper.search import search_google, search_from_url

async def test_google_search_with_captcha_detection():
    """Test Google search with CAPTCHA detection."""
    print("🔍 Testing Google search with CAPTCHA detection...")
    print("=" * 50)
    
    # Test 1: Simple Google search
    print("\n1. Testing simple Google search:")
    try:
        results = await search_google("python programming", max_results=5)
        print(f"   Found {len(results)} results")
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Search from URL with CAPTCHA detection
    print("\n2. Testing search from URL:")
    try:
        google_url = "https://www.google.com/search?q=artificial+intelligence&hl=en&gl=us"
        results = await search_from_url(google_url, provider="google", max_results=5)
        print(f"   Found {len(results)} results")
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result.get('url', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n✅ CAPTCHA detection is active!")
    print("   If Google shows a CAPTCHA, the script will:")
    print("   - Detect it automatically")
    print("   - Print a warning message")
    print("   - Wait for you to solve it manually")
    print("   - Continue after you press Enter")

if __name__ == "__main__":
    asyncio.run(test_google_search_with_captcha_detection())

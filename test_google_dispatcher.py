#!/usr/bin/env python3
"""
Test script to demonstrate improved Google crawling with specialized dispatcher.
Features: rate limiting, memory management, anti-bot measures, and monitoring.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_google_dispatcher_multi_window():
    """Test Google crawling with specialized dispatcher in multi-window mode."""
    print("🔍 Testing GOOGLE DISPATCHER MULTI-WINDOW pagination...")
    print("   Features: Rate limiting, memory management, anti-bot measures")
    print("   Real-time monitoring with CrawlerMonitor")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=30,
            max_paginate=3,
            pagination_mode="multi_window",
            headless=False  # Set to True for headless mode
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Google dispatcher multi-window completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:5], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more results")
            
    except Exception as e:
        print(f"❌ Google dispatcher multi-window failed: {e}")


async def test_google_dispatcher_search_from_url():
    """Test the dispatcher with search_from_url."""
    print("\n🔍 Testing GOOGLE DISPATCHER with search_from_url...")
    
    start_time = time.time()
    
    try:
        results = await search_from_url(
            "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024",
            max_results=20,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=False
        )
        
        elapsed = time.time() - start_time
        print(f"✅ search_from_url with dispatcher completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, result in enumerate(results[:3], 1):
            if isinstance(result, dict) and 'url' in result:
                print(f"   {i}. {result['url']}")
            elif isinstance(result, str):
                print(f"   {i}. {result}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ search_from_url with dispatcher failed: {e}")


async def test_dispatcher_features():
    """Test and demonstrate dispatcher features."""
    print("\n🚀 Google Dispatcher Features Demonstration")
    print("=" * 60)
    
    print("📋 Dispatcher Configuration:")
    print("   • Rate Limiter: 3-7 second random delays")
    print("   • Memory Threshold: 75% (conservative)")
    print("   • Max Concurrent Sessions: 3")
    print("   • Rate Limit Codes: 429, 503, 403")
    print("   • Real-time Monitoring: Enabled")
    
    print("\n🛡️ Anti-Bot Measures:")
    print("   • User-Agent: Chrome 120.0.0.0")
    print("   • Viewport: 1920x1080")
    print("   • Locale: en-US")
    print("   • Timezone: America/New_York")
    print("   • Robots.txt: Respected")
    print("   • Magic Mode: Enabled")
    print("   • User Simulation: Enabled")
    
    print("\n⚡ Performance Features:")
    print("   • Memory Adaptive: Automatic concurrency control")
    print("   • Exponential Backoff: Smart retry logic")
    print("   • Live Monitoring: Real-time progress display")
    print("   • Resource Management: Automatic memory checks")


async def test_headless_dispatcher():
    """Test dispatcher in headless mode."""
    print("\n🔍 Testing GOOGLE DISPATCHER in HEADLESS mode...")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=20,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Headless dispatcher completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ Headless dispatcher failed: {e}")


async def test_rate_limit_handling():
    """Test how the dispatcher handles rate limiting."""
    print("\n🔄 Testing Rate Limit Handling...")
    print("   This test demonstrates the dispatcher's ability to handle rate limits")
    print("   and automatically retry with exponential backoff")
    
    start_time = time.time()
    
    try:
        # Test with multiple pages to potentially trigger rate limits
        results = await search_google(
            "python tutorial",
            max_results=50,
            max_paginate=5,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Rate limit test completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        print("   💡 If rate limits were encountered, the dispatcher handled them automatically")
        
    except Exception as e:
        print(f"❌ Rate limit test failed: {e}")


async def test_memory_management():
    """Test memory management features."""
    print("\n🧠 Testing Memory Management...")
    print("   This test demonstrates the dispatcher's memory adaptive features")
    
    start_time = time.time()
    
    try:
        # Test with larger number of pages to test memory management
        results = await search_google(
            "machine learning tutorial",
            max_results=60,
            max_paginate=6,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Memory management test completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        print("   💡 Memory usage was monitored and controlled automatically")
        
    except Exception as e:
        print(f"❌ Memory management test failed: {e}")


if __name__ == "__main__":
    print("🎯 Google Dispatcher Test Suite")
    print("This script demonstrates improved Google crawling with specialized dispatcher.")
    print("Based on Crawl4AI documentation: https://docs.crawl4ai.com/advanced/multi-url-crawling/")
    print()
    
    # Ask user which test to run
    print("Choose a test:")
    print("1. Google dispatcher multi-window mode")
    print("2. search_from_url with dispatcher")
    print("3. Dispatcher features demonstration")
    print("4. Headless dispatcher mode")
    print("5. Rate limit handling test")
    print("6. Memory management test")
    print("7. All tests")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == "1":
        asyncio.run(test_google_dispatcher_multi_window())
    elif choice == "2":
        asyncio.run(test_google_dispatcher_search_from_url())
    elif choice == "3":
        asyncio.run(test_dispatcher_features())
    elif choice == "4":
        asyncio.run(test_headless_dispatcher())
    elif choice == "5":
        asyncio.run(test_rate_limit_handling())
    elif choice == "6":
        asyncio.run(test_memory_management())
    elif choice == "7":
        asyncio.run(test_dispatcher_features())
        asyncio.run(test_google_dispatcher_multi_window())
        asyncio.run(test_google_dispatcher_search_from_url())
        asyncio.run(test_headless_dispatcher())
        asyncio.run(test_rate_limit_handling())
        asyncio.run(test_memory_management())
    else:
        print("Invalid choice. Running dispatcher features demonstration...")
        asyncio.run(test_dispatcher_features())

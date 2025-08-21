#!/usr/bin/env python3
"""
Test script to demonstrate the improved arun_many pagination for Google search.
This uses arun_many for better performance in multi-window mode.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_arun_many_multi_window():
    """Test the improved arun_many multi-window pagination."""
    print("🔍 Testing ARUN_MANY MULTI-WINDOW pagination...")
    print("   This uses arun_many for parallel processing")
    print("   Better performance than individual tasks")
    
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
        print(f"✅ arun_many multi-window mode completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:5], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more results")
            
    except Exception as e:
        print(f"❌ arun_many multi-window mode failed: {e}")


async def test_arun_many_search_from_url():
    """Test the improved arun_many with search_from_url."""
    print("\n🔍 Testing ARUN_MANY search_from_url with multi-window pagination...")
    
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
        print(f"✅ search_from_url arun_many completed in {elapsed:.2f} seconds")
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
        print(f"❌ search_from_url arun_many failed: {e}")


async def test_comparison_arun_many():
    """Compare arun_many multi-window with single-window modes."""
    print("🚀 Starting arun_many pagination comparison...")
    print("=" * 60)
    
    # Test arun_many multi-window mode
    await test_arun_many_multi_window()
    
    print("\n" + "=" * 60)
    
    # Test single-window mode
    print("🔍 Testing SINGLE-WINDOW pagination...")
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=30,
            max_paginate=3,
            pagination_mode="single_window",
            headless=False
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Single-window mode completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Single-window mode failed: {e}")
    
    print("\n" + "=" * 60)
    print("📋 arun_many Multi-Window Features:")
    print("   • Parallel processing with arun_many")
    print("   • Better performance than individual tasks")
    print("   • CAPTCHA handling for each page")
    print("   • Automatic URL deduplication")
    print("   • Error handling per page")


async def test_headless_arun_many():
    """Test arun_many multi-window mode in headless mode."""
    print("\n🔍 Testing ARUN_MANY multi-window mode in HEADLESS mode...")
    
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
        print(f"✅ Headless arun_many multi-window completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ Headless arun_many multi-window failed: {e}")


async def test_performance_comparison():
    """Compare performance between different pagination modes."""
    print("\n🚀 Performance Comparison Test")
    print("=" * 60)
    
    test_configs = [
        ("Multi-window (arun_many)", "multi_window", False),
        ("Single-window (JavaScript)", "single_window", False),
        ("Headless Multi-window", "multi_window", True),
        ("Headless Single-window", "single_window", True),
    ]
    
    for name, mode, headless in test_configs:
        print(f"\n🔍 Testing {name}...")
        start_time = time.time()
        
        try:
            results = await search_google(
                "travel card site:pantip.com after:2024",
                max_results=20,
                max_paginate=2,
                pagination_mode=mode,
                headless=headless
            )
            
            elapsed = time.time() - start_time
            print(f"   ✅ {name}: {elapsed:.2f}s, {len(results)} results")
            
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"   ❌ {name}: {elapsed:.2f}s, Error: {e}")


if __name__ == "__main__":
    print("🎯 arun_many Google Search Pagination Test")
    print("This script demonstrates the improved arun_many pagination.")
    print("Features: parallel processing, better performance, CAPTCHA handling")
    print()
    
    # Ask user which test to run
    print("Choose a test:")
    print("1. arun_many multi-window mode")
    print("2. search_from_url with arun_many")
    print("3. Comparison (arun_many vs single-window)")
    print("4. Headless arun_many multi-window")
    print("5. Performance comparison")
    print("6. All tests")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        asyncio.run(test_arun_many_multi_window())
    elif choice == "2":
        asyncio.run(test_arun_many_search_from_url())
    elif choice == "3":
        asyncio.run(test_comparison_arun_many())
    elif choice == "4":
        asyncio.run(test_headless_arun_many())
    elif choice == "5":
        asyncio.run(test_performance_comparison())
    elif choice == "6":
        asyncio.run(test_comparison_arun_many())
        asyncio.run(test_arun_many_search_from_url())
        asyncio.run(test_headless_arun_many())
        asyncio.run(test_performance_comparison())
    else:
        print("Invalid choice. Running arun_many multi-window test...")
        asyncio.run(test_arun_many_multi_window())

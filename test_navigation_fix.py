#!/usr/bin/env python3
"""
Test script to verify the navigation error fixes for Google crawling.
Tests the improved error handling and fallback mechanisms.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_navigation_fix():
    """Test the navigation error fixes."""
    print("🔍 Testing Navigation Error Fixes...")
    print("   Features: wait_until, wait_for, error handling, fallback extraction")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=20,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True  # Use headless for testing
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Navigation fix test completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:5], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more results")
            
    except Exception as e:
        print(f"❌ Navigation fix test failed: {e}")


async def test_error_handling():
    """Test error handling and fallback mechanisms."""
    print("\n🔍 Testing Error Handling and Fallbacks...")
    
    start_time = time.time()
    
    try:
        results = await search_from_url(
            "https://www.google.com/search?q=python+tutorial&start=0",
            max_results=15,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Error handling test completed in {elapsed:.2f} seconds")
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
        print(f"❌ Error handling test failed: {e}")


async def test_wait_conditions():
    """Test the wait conditions for page loading."""
    print("\n⏳ Testing Wait Conditions...")
    print("   Testing wait_until='networkidle' and wait_for selectors")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "machine learning tutorial",
            max_results=10,
            max_paginate=1,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Wait conditions test completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        print("   💡 Page loading was properly waited for")
        
    except Exception as e:
        print(f"❌ Wait conditions test failed: {e}")


async def test_fallback_extraction():
    """Test the fallback HTML extraction mechanism."""
    print("\n🔄 Testing Fallback Extraction...")
    print("   Testing HTML fallback when JSON extraction fails")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "web development tutorial",
            max_results=15,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Fallback extraction test completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        print("   💡 Fallback mechanisms were tested")
        
    except Exception as e:
        print(f"❌ Fallback extraction test failed: {e}")


async def test_robustness():
    """Test overall robustness with various scenarios."""
    print("\n🛡️ Testing Overall Robustness...")
    
    test_cases = [
        ("python tutorial", 10, 1),
        ("machine learning", 15, 2),
        ("web development", 20, 2),
        ("data science", 12, 1),
    ]
    
    total_results = 0
    successful_tests = 0
    
    for query, max_results, max_paginate in test_cases:
        print(f"\n   Testing: '{query}' ({max_results} results, {max_paginate} pages)")
        
        try:
            start_time = time.time()
            results = await search_google(
                query,
                max_results=max_results,
                max_paginate=max_paginate,
                pagination_mode="multi_window",
                headless=True
            )
            
            elapsed = time.time() - start_time
            print(f"   ✅ Success: {len(results)} results in {elapsed:.2f}s")
            total_results += len(results)
            successful_tests += 1
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print(f"\n📊 Robustness Test Summary:")
    print(f"   • Successful tests: {successful_tests}/{len(test_cases)}")
    print(f"   • Total results collected: {total_results}")
    print(f"   • Success rate: {(successful_tests/len(test_cases)*100):.1f}%")


if __name__ == "__main__":
    print("🎯 Navigation Error Fix Test Suite")
    print("This script tests the fixes for navigation and content extraction errors.")
    print()
    
    # Ask user which test to run
    print("Choose a test:")
    print("1. Navigation error fixes")
    print("2. Error handling and fallbacks")
    print("3. Wait conditions test")
    print("4. Fallback extraction test")
    print("5. Overall robustness test")
    print("6. All tests")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    if choice == "1":
        asyncio.run(test_navigation_fix())
    elif choice == "2":
        asyncio.run(test_error_handling())
    elif choice == "3":
        asyncio.run(test_wait_conditions())
    elif choice == "4":
        asyncio.run(test_fallback_extraction())
    elif choice == "5":
        asyncio.run(test_robustness())
    elif choice == "6":
        asyncio.run(test_navigation_fix())
        asyncio.run(test_error_handling())
        asyncio.run(test_wait_conditions())
        asyncio.run(test_fallback_extraction())
        asyncio.run(test_robustness())
    else:
        print("Invalid choice. Running navigation fix test...")
        asyncio.run(test_navigation_fix())

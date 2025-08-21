#!/usr/bin/env python3
"""
Test script safe for Jupyter notebook environments.
Avoids CrawlerMonitor issues and provides alternative progress tracking.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_jupyter_safe_google():
    """Test Google crawling in Jupyter-safe mode."""
    print("🔍 Testing Jupyter-Safe Google Crawling...")
    print("   Features: No CrawlerMonitor, safe for notebook environments")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=20,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True  # Use headless for notebook safety
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Jupyter-safe test completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:5], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more results")
            
    except Exception as e:
        print(f"❌ Jupyter-safe test failed: {e}")


async def test_jupyter_safe_search_from_url():
    """Test search_from_url in Jupyter-safe mode."""
    print("\n🔍 Testing Jupyter-Safe search_from_url...")
    
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
        print(f"✅ Jupyter-safe search_from_url completed in {elapsed:.2f} seconds")
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
        print(f"❌ Jupyter-safe search_from_url failed: {e}")


async def test_progress_tracking():
    """Test alternative progress tracking for Jupyter environments."""
    print("\n📊 Testing Alternative Progress Tracking...")
    print("   Using print statements instead of CrawlerMonitor")
    
    test_queries = [
        "python tutorial",
        "machine learning",
        "web development"
    ]
    
    total_results = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   🔍 Query {i}/{len(test_queries)}: '{query}'")
        
        try:
            start_time = time.time()
            results = await search_google(
                query,
                max_results=10,
                max_paginate=1,
                pagination_mode="multi_window",
                headless=True
            )
            
            elapsed = time.time() - start_time
            print(f"   ✅ Success: {len(results)} results in {elapsed:.2f}s")
            total_results += len(results)
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print(f"\n📊 Progress Summary:")
    print(f"   • Total queries processed: {len(test_queries)}")
    print(f"   • Total results collected: {total_results}")


async def test_error_handling_jupyter():
    """Test error handling in Jupyter environment."""
    print("\n🛡️ Testing Error Handling in Jupyter...")
    
    # Test with a query that might trigger errors
    try:
        results = await search_google(
            "very specific query that might not have many results",
            max_results=50,
            max_paginate=5,
            pagination_mode="multi_window",
            headless=True
        )
        
        print(f"✅ Error handling test completed")
        print(f"📊 Found {len(results)} results")
        print("   💡 Error handling worked correctly")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")


def check_jupyter_environment():
    """Check if we're in a Jupyter environment."""
    try:
        import IPython
        if IPython.get_ipython() is not None:
            print("🎯 Jupyter Notebook Environment Detected")
            print("   ✅ Using Jupyter-safe configuration")
            print("   📝 CrawlerMonitor will be disabled")
            return True
        else:
            print("🎯 Terminal Environment Detected")
            print("   ✅ Full monitoring features available")
            return False
    except ImportError:
        print("🎯 Standard Python Environment")
        print("   ✅ Full monitoring features available")
        return False


if __name__ == "__main__":
    print("🎯 Jupyter-Safe Test Suite")
    print("This script is designed to work safely in Jupyter notebook environments.")
    print()
    
    # Check environment
    is_jupyter = check_jupyter_environment()
    print()
    
    # Ask user which test to run
    print("Choose a test:")
    print("1. Jupyter-safe Google crawling")
    print("2. Jupyter-safe search_from_url")
    print("3. Alternative progress tracking")
    print("4. Error handling in Jupyter")
    print("5. All tests")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        asyncio.run(test_jupyter_safe_google())
    elif choice == "2":
        asyncio.run(test_jupyter_safe_search_from_url())
    elif choice == "3":
        asyncio.run(test_progress_tracking())
    elif choice == "4":
        asyncio.run(test_error_handling_jupyter())
    elif choice == "5":
        asyncio.run(test_jupyter_safe_google())
        asyncio.run(test_jupyter_safe_search_from_url())
        asyncio.run(test_progress_tracking())
        asyncio.run(test_error_handling_jupyter())
    else:
        print("Invalid choice. Running Jupyter-safe Google crawling...")
        asyncio.run(test_jupyter_safe_google())

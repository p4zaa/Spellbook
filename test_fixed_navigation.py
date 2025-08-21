#!/usr/bin/env python3
"""
Test script to verify the fixed navigation logic and arun_many error handling.
Tests the go back functionality and ensures arun_many works properly.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_fixed_navigation():
    """Test the fixed navigation logic with go back functionality."""
    print("🔄 Testing Fixed Navigation Logic")
    print("   Strategy: Check for results, go back if not found")
    print("   Features: Fixed wait_for logic, arun_many error handling")
    print()
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "python tutorial",
            max_results=10,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Fixed navigation completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ Fixed navigation failed: {e}")
        import traceback
        traceback.print_exc()


async def test_single_window_navigation():
    """Test single-window navigation with go back functionality."""
    print("\n🔄 Testing Single-Window Navigation...")
    print("   Strategy: JavaScript pagination with go back logic")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "machine learning tutorial",
            max_results=15,
            max_paginate=2,
            pagination_mode="single_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Single-window navigation completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Single-window navigation failed: {e}")
        import traceback
        traceback.print_exc()


async def test_arun_many_error_handling():
    """Test arun_many error handling with multiple URLs."""
    print("\n🪟 Testing arun_many Error Handling...")
    print("   Strategy: Multiple URLs with fallback to individual requests")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "web scraping tutorial",
            max_results=20,
            max_paginate=3,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ arun_many error handling completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ arun_many error handling failed: {e}")
        import traceback
        traceback.print_exc()


def explain_fixes():
    """Explain the fixes made to the navigation logic."""
    print("\n🔧 Navigation Logic Fixes")
    print("=" * 40)
    
    print("\n❌ Previous Issues:")
    print("   • wait_for logic had async/await in synchronous function")
    print("   • arun_many returning NoneType causing iteration errors")
    print("   • magic=True and simulate_user=True were disabled")
    print("   • No proper error handling for arun_many failures")
    
    print("\n✅ Fixes Applied:")
    print("   • Fixed wait_for to return boolean only")
    print("   • Added NoneType check for arun_many results")
    print("   • Re-enabled magic=True and simulate_user=True")
    print("   • Added proper fallback to individual requests")
    print("   • Enhanced error handling and logging")
    
    print("\n🛡️ Safety Measures:")
    print("   • Results type validation")
    print("   • Graceful fallback mechanisms")
    print("   • Comprehensive error logging")
    print("   • Browser history navigation")
    
    print("\n📊 Benefits:")
    print("   • More reliable crawling")
    print("   • Better error recovery")
    print("   • Improved anti-bot handling")
    print("   • Consistent results extraction")


def show_wait_for_fix():
    """Show the wait_for logic fix."""
    print("\n🔧 Wait_For Logic Fix")
    print("=" * 30)
    
    print("\n❌ Before (Broken):")
    print("   ```javascript")
    print("   () => {")
    print("       const resultsExist = document.querySelector('#rso, .g, .MjjYud');")
    print("       if (resultsExist) {")
    print("           return true;")
    print("       } else {")
    print("           window.history.back();  // ❌ Navigation in wait_for")
    print("           await new Promise(...); // ❌ async in sync function")
    print("           return false;")
    print("       }")
    print("   }")
    print("   ```")
    
    print("\n✅ After (Fixed):")
    print("   ```javascript")
    print("   () => {")
    print("       const resultsExist = document.querySelector('#rso, .g, .MjjYud');")
    print("       return resultsExist !== null; // ✅ Boolean only")
    print("   }")
    print("   ```")
    
    print("\n📝 Navigation Logic Moved To:")
    print("   • js_code: Handles navigation and go back")
    print("   • wait_for: Only checks for elements")
    print("   • Proper separation of concerns")


def show_arun_many_fix():
    """Show the arun_many error handling fix."""
    print("\n🪟 arun_many Error Handling Fix")
    print("=" * 40)
    
    print("\n❌ Before (Broken):")
    print("   ```python")
    print("   results = await crawler.arun_many(urls, config, dispatcher)")
    print("   for result in results:  # ❌ Fails if results is None")
    print("       # Process result")
    print("   ```")
    
    print("\n✅ After (Fixed):")
    print("   ```python")
    print("   results = await crawler.arun_many(urls, config, dispatcher)")
    print("   if results is None:")
    print("       print('arun_many returned None, falling back...')")
    print("       results = []")
    print("       for url in urls:")
    print("           result = await crawler.arun(url, config)")
    print("           results.append(result)")
    print("   elif not isinstance(results, list):")
    print("       print('Unexpected type, using empty list')")
    print("       results = []")
    print("   ```")
    
    print("\n🛡️ Safety Checks:")
    print("   • NoneType validation")
    print("   • Type checking")
    print("   • Graceful fallback")
    print("   • Error logging")


if __name__ == "__main__":
    print("🔧 Fixed Navigation Logic Test Suite")
    print("This script tests the fixes for navigation logic and arun_many errors.")
    print()
    
    # Explain the fixes
    explain_fixes()
    show_wait_for_fix()
    show_arun_many_fix()
    
    print("\n" + "=" * 60)
    
    # Ask user which test to run
    print("\nChoose a test:")
    print("1. Basic fixed navigation test")
    print("2. Single-window navigation test")
    print("3. arun_many error handling test")
    print("4. All tests")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(test_fixed_navigation())
    elif choice == "2":
        asyncio.run(test_single_window_navigation())
    elif choice == "3":
        asyncio.run(test_arun_many_error_handling())
    elif choice == "4":
        asyncio.run(test_fixed_navigation())
        asyncio.run(test_single_window_navigation())
        asyncio.run(test_arun_many_error_handling())
    else:
        print("Invalid choice. Running basic fixed navigation test...")
        asyncio.run(test_fixed_navigation())

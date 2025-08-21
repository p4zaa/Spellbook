#!/usr/bin/env python3
"""
Test script to demonstrate the new pagination modes for Google search.
Shows the difference between multi_window (default) and single_window modes.
"""

import asyncio
import time
from spellbook.scraper.search import search_google


async def test_multi_window_mode():
    """Test the traditional multi-window pagination mode."""
    print("🔍 Testing MULTI-WINDOW pagination mode...")
    print("   This opens separate browser windows for each page")
    print("   Each window may require separate CAPTCHA solving")
    
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
        print(f"✅ Multi-window mode completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:5], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more results")
            
    except Exception as e:
        print(f"❌ Multi-window mode failed: {e}")


async def test_single_window_mode():
    """Test the new single-window pagination mode."""
    print("\n🔍 Testing SINGLE-WINDOW pagination mode...")
    print("   This uses JavaScript to click 'next page' buttons in the same window")
    print("   Only one CAPTCHA solving session needed for all pages")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=30,
            max_paginate=3,
            pagination_mode="single_window",
            headless=False  # Set to True for headless mode
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Single-window mode completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:5], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 5:
            print(f"   ... and {len(results) - 5} more results")
            
    except Exception as e:
        print(f"❌ Single-window mode failed: {e}")


async def test_comparison():
    """Compare both modes side by side."""
    print("🚀 Starting pagination mode comparison...")
    print("=" * 60)
    
    # Test multi-window mode
    await test_multi_window_mode()
    
    print("\n" + "=" * 60)
    
    # Test single-window mode
    await test_single_window_mode()
    
    print("\n" + "=" * 60)
    print("📋 Summary:")
    print("   • Multi-window: Opens separate browser windows for each page")
    print("   • Single-window: Uses JavaScript to navigate within one window")
    print("   • Single-window is better for CAPTCHA handling (only one session)")
    print("   • Multi-window is more reliable but may trigger more CAPTCHAs")


async def test_headless_single_window():
    """Test single-window mode in headless mode."""
    print("\n🔍 Testing SINGLE-WINDOW mode in HEADLESS mode...")
    print("   This demonstrates the JavaScript pagination without visible browser")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=20,
            max_paginate=2,
            pagination_mode="single_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Headless single-window mode completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ Headless single-window mode failed: {e}")


if __name__ == "__main__":
    print("🎯 Google Search Pagination Mode Test")
    print("This script demonstrates the new pagination modes for Google search.")
    print()
    
    # Ask user which test to run
    print("Choose a test:")
    print("1. Multi-window mode (traditional)")
    print("2. Single-window mode (new)")
    print("3. Comparison of both modes")
    print("4. Headless single-window mode")
    print("5. All tests")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        asyncio.run(test_multi_window_mode())
    elif choice == "2":
        asyncio.run(test_single_window_mode())
    elif choice == "3":
        asyncio.run(test_comparison())
    elif choice == "4":
        asyncio.run(test_headless_single_window())
    elif choice == "5":
        asyncio.run(test_comparison())
        asyncio.run(test_headless_single_window())
    else:
        print("Invalid choice. Running comparison test...")
        asyncio.run(test_comparison())

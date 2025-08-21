#!/usr/bin/env python3
"""
Test script to demonstrate proper timing approach for wait_for with simulate_user.
Shows how to ensure elements are detected before user simulation starts.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url


async def test_timing_approach():
    """Test the timing approach: wait_for BEFORE simulate_user."""
    print("⏰ Testing Timing Approach: Wait_For BEFORE Simulate_User")
    print("   Strategy: Detect elements first, then enable user simulation")
    print()
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "travel card site:pantip.com after:2024",
            max_results=15,
            max_paginate=2,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Timing approach completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
        # Show first few results
        for i, url in enumerate(results[:3], 1):
            print(f"   {i}. {url}")
        
        if len(results) > 3:
            print(f"   ... and {len(results) - 3} more results")
            
    except Exception as e:
        print(f"❌ Timing approach failed: {e}")


async def test_single_window_timing():
    """Test timing approach with single-window pagination."""
    print("\n🔄 Testing Single-Window Timing Approach...")
    print("   Strategy: JavaScript pagination with proper timing")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "python tutorial",
            max_results=20,
            max_paginate=3,
            pagination_mode="single_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Single-window timing completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Single-window timing failed: {e}")


async def test_multi_window_timing():
    """Test timing approach with multi-window pagination."""
    print("\n🪟 Testing Multi-Window Timing Approach...")
    print("   Strategy: Separate windows with proper timing")
    
    start_time = time.time()
    
    try:
        results = await search_google(
            "machine learning tutorial",
            max_results=20,
            max_paginate=3,
            pagination_mode="multi_window",
            headless=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Multi-window timing completed in {elapsed:.2f} seconds")
        print(f"📊 Found {len(results)} results")
        
    except Exception as e:
        print(f"❌ Multi-window timing failed: {e}")


def explain_timing_approach():
    """Explain the timing approach for wait_for with simulate_user."""
    print("\n📚 Understanding the Timing Approach")
    print("=" * 50)
    
    print("\n🎯 The Problem:")
    print("   • simulate_user=True can modify page content")
    print("   • wait_for needs to detect elements BEFORE they're modified")
    print("   • Timing conflicts between element detection and user simulation")
    
    print("\n⚡ The Solution:")
    print("   • Configure wait_for BEFORE enabling simulate_user")
    print("   • Use proper wait conditions (networkidle)")
    print("   • Ensure elements are detected before user simulation starts")
    
    print("\n🔧 Implementation:")
    print("   • wait_until='networkidle' - Wait for network to be idle")
    print("   • wait_for='#rso, .g, .MjjYud' - Wait for search results")
    print("   • simulate_user=True - Enable after elements are detected")
    print("   • magic=True - Enable page optimizations")
    
    print("\n📊 Benefits:")
    print("   • Reliable element detection")
    print("   • No timing conflicts")
    print("   • Better anti-bot protection")
    print("   • Consistent results")


def compare_approaches():
    """Compare different approaches to handling wait_for with simulate_user."""
    print("\n🔄 Approach Comparison")
    print("=" * 40)
    
    approaches = [
        {
            "name": "❌ Bad: Wait_For After Simulate_User",
            "description": "Enable simulate_user first, then wait_for",
            "issues": ["Elements might be modified", "Timing conflicts", "Unreliable detection"]
        },
        {
            "name": "✅ Good: Wait_For Before Simulate_User",
            "description": "Configure wait_for first, then enable simulate_user",
            "benefits": ["Reliable element detection", "No timing conflicts", "Consistent results"]
        },
        {
            "name": "🛡️ Better: Safe Anti-Bot Measures",
            "description": "Use alternatives to simulate_user",
            "benefits": ["No interference with wait_for", "Still effective anti-bot", "More predictable"]
        }
    ]
    
    for i, approach in enumerate(approaches, 1):
        print(f"\n{i}. {approach['name']}")
        print(f"   {approach['description']}")
        
        if "issues" in approach:
            print("   Issues:")
            for issue in approach["issues"]:
                print(f"      • {issue}")
        
        if "benefits" in approach:
            print("   Benefits:")
            for benefit in approach["benefits"]:
                print(f"      • {benefit}")


if __name__ == "__main__":
    print("⏰ Timing Approach Test Suite")
    print("This script demonstrates proper timing for wait_for with simulate_user.")
    print()
    
    # Explain the approach
    explain_timing_approach()
    compare_approaches()
    
    print("\n" + "=" * 60)
    
    # Ask user which test to run
    print("\nChoose a test:")
    print("1. Basic timing approach test")
    print("2. Single-window timing test")
    print("3. Multi-window timing test")
    print("4. All timing tests")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        asyncio.run(test_timing_approach())
    elif choice == "2":
        asyncio.run(test_single_window_timing())
    elif choice == "3":
        asyncio.run(test_multi_window_timing())
    elif choice == "4":
        asyncio.run(test_timing_approach())
        asyncio.run(test_single_window_timing())
        asyncio.run(test_multi_window_timing())
    else:
        print("Invalid choice. Running basic timing test...")
        asyncio.run(test_timing_approach())

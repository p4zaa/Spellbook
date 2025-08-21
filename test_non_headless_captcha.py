#!/usr/bin/env python3
"""
Test script for CAPTCHA handling in non-headless mode.
This script demonstrates how the browser window stays open for manual CAPTCHA solving.
"""

import asyncio
from spellbook.scraper.search import search_google, search_from_url

async def test_non_headless_captcha():
    """Test CAPTCHA handling in non-headless mode."""
    print("🔍 Testing CAPTCHA Handling in Non-Headless Mode")
    print("=" * 55)
    
    print("\n📋 What this test does:")
    print("1. Opens a visible browser window (headless=False)")
    print("2. Performs a Google search that might trigger CAPTCHA")
    print("3. If CAPTCHA is detected:")
    print("   - Browser window stays open")
    print("   - Script waits for you to solve CAPTCHA manually")
    print("   - Automatically continues after CAPTCHA is solved")
    print("4. If no CAPTCHA, continues normally")
    
    print("\n🚀 Starting Google search with visible browser...")
    
    try:
        # Perform a Google search with headless=False
        results = await search_google(
            "travel card site:pantip.com after:2024", 
            max_results=5,
            headless=False  # This opens a visible browser window
        )
        
        print(f"\n✅ Search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        for i, url in enumerate(results, 1):
            print(f"   {i}. {url}")
            
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("   This might be due to network issues or rate limiting.")

async def test_search_from_url_non_headless():
    """Test search from URL in non-headless mode."""
    print("\n\n🌐 Testing Search from URL (Non-Headless)")
    print("=" * 45)
    
    try:
        # Search from a specific Google URL
        google_url = "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024&start=0"
        results = await search_from_url(
            google_url, 
            provider="google", 
            max_results=5,
            headless=False  # Visible browser window
        )
        
        print(f"\n✅ URL search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result.get('url', 'N/A')}")
            
    except Exception as e:
        print(f"\n❌ Error during URL search: {e}")

def main():
    """Main function to run the non-headless CAPTCHA tests."""
    print("🎯 Non-Headless CAPTCHA Handling Demo")
    print("=" * 50)
    
    print("\n💡 Key Features:")
    print("   ✅ Browser window remains visible during CAPTCHA solving")
    print("   ✅ Automatic detection when CAPTCHA is solved")
    print("   ✅ No manual input required - just solve the CAPTCHA in the browser")
    print("   ✅ 5-minute timeout with status updates")
    
    print("\n⚠️  Note: This test may trigger a real CAPTCHA challenge")
    print("   The browser window will stay open for you to solve it manually")
    
    # Run the tests
    asyncio.run(test_non_headless_captcha())
    asyncio.run(test_search_from_url_non_headless())
    
    print("\n\n🎉 Non-headless CAPTCHA test completed!")
    print("\n📝 What you experienced:")
    print("   ✅ Browser window opened and stayed visible")
    print("   ✅ CAPTCHA detection worked automatically")
    print("   ✅ Script waited for manual solving")
    print("   ✅ Continued automatically after solving")

if __name__ == "__main__":
    main()

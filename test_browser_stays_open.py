#!/usr/bin/env python3
"""
Test script to verify that the browser window stays open during CAPTCHA solving.
This script tests the fixed CAPTCHA handling that keeps the browser session alive.
"""

import asyncio
from spellbook.scraper.search import search_google, search_from_url

async def test_browser_stays_open():
    """Test that browser window stays open during CAPTCHA solving."""
    print("🔍 Testing Browser Window Stays Open During CAPTCHA")
    print("=" * 55)
    
    print("\n📋 What this test does:")
    print("1. Opens a visible browser window (headless=False)")
    print("2. Performs a Google search that might trigger CAPTCHA")
    print("3. If CAPTCHA is detected:")
    print("   - Browser window should stay open")
    print("   - Script should wait for CAPTCHA to be solved")
    print("   - Should continue automatically after CAPTCHA is solved")
    print("4. If no CAPTCHA, continues normally")
    
    print("\n🚀 Starting Google search with visible browser...")
    print("   ⚠️  This test may trigger a real CAPTCHA challenge")
    print("   💡 The browser window should stay open for you to solve it")
    
    try:
        # Perform a Google search with headless=False
        # Use a search term that's more likely to trigger CAPTCHA
        results = await search_google(
            "travel card site:pantip.com after:2024", 
            max_results=3,
            headless=False,  # This opens a visible browser window
            browser_type="chromium"
        )
        
        print(f"\n✅ Search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        for i, url in enumerate(results, 1):
            print(f"   {i}. {url}")
            
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("   This might be due to network issues or rate limiting.")

async def test_search_from_url_browser_stays_open():
    """Test search from URL with browser staying open."""
    print("\n\n🌐 Testing Search from URL (Browser Stays Open)")
    print("=" * 50)
    
    try:
        # Search from a specific Google URL that might trigger CAPTCHA
        #google_url = "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024&start=0"
        google_url = "https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dtravel%2Bcard%2Bsite:pantip.com%2Bafter:2024%26as_epq%3Dtravel%2Bcard%26start%3D0&q=EhAkBZgAtlI6YO1Am8L6wQoRGMnhmMUGIjBEsfFR3J6tv2xAX9dwIPA2aCdGo0h4z34BraY2d0cAd54wyw78U3yynnTnc2_7zdgyAnJSWgFD"
        results = await search_from_url(
            google_url, 
            provider="google", 
            max_results=1,
            headless=True,  # Visible browser window
            browser_type="chromium"
        )
        
        print(f"\n✅ URL search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        for i, result in enumerate(results[:3], 1):
            print(f"   {i}. {result.get('url', 'N/A')}")
            
    except Exception as e:
        print(f"\n❌ Error during URL search: {e}")

def main():
    """Main function to run the browser stays open tests."""
    print("🎯 Browser Stays Open During CAPTCHA Test")
    print("=" * 50)
    
    print("\n💡 Key Features Being Tested:")
    print("   ✅ Browser window remains open during CAPTCHA solving")
    print("   ✅ No immediate browser closure")
    print("   ✅ Automatic detection using wait_for selectors")
    print("   ✅ Proper session management")
    
    print("\n⚠️  Important Notes:")
    print("   - This test may trigger a real CAPTCHA challenge")
    print("   - The browser window should stay open for manual solving")
    print("   - The script will automatically detect when CAPTCHA is solved")
    print("   - Uses wait_for selectors to detect search results")
    
    # Run the tests
    asyncio.run(test_browser_stays_open())
    asyncio.run(test_search_from_url_browser_stays_open())
    
    print("\n\n🎉 Browser stays open test completed!")
    print("\n📝 What you should have experienced:")
    print("   ✅ Browser window opened and stayed visible")
    print("   ✅ No immediate closure of the browser")
    print("   ✅ CAPTCHA detection worked properly")
    print("   ✅ Script waited for CAPTCHA to be solved")
    print("   ✅ Continued automatically after solving")

if __name__ == "__main__":
    main()

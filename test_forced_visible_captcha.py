#!/usr/bin/env python3
"""
Test script to demonstrate forced visible window for CAPTCHA solving.
This script shows how the browser window becomes visible for CAPTCHA solving
even when the main script is running in headless mode.
"""

import asyncio
from spellbook.scraper.search import search_google, search_from_url

async def test_headless_with_visible_captcha():
    """Test that headless mode shows visible window for CAPTCHA solving."""
    print("🔍 Testing Headless Mode with Forced Visible CAPTCHA Window")
    print("=" * 65)
    
    print("\n📋 What this test does:")
    print("1. Runs in headless mode (headless=True)")
    print("2. Performs a Google search that might trigger CAPTCHA")
    print("3. If CAPTCHA is detected:")
    print("   - Forces browser window to be visible (headless=False)")
    print("   - Allows manual CAPTCHA solving")
    print("   - Uses 5-minute timeout (same as non-headless)")
    print("   - Automatically detects when CAPTCHA is solved")
    print("4. If no CAPTCHA, continues normally")
    
    print("\n🚀 Starting Google search in headless mode...")
    print("   ⚠️  This test may trigger a real CAPTCHA challenge")
    print("   💡 Even though main script is headless, CAPTCHA window will be visible")
    
    try:
        # Perform a Google search with headless=True
        results = await search_google(
            "travel card site:pantip.com after:2024", 
            max_results=3,
            headless=True,  # Main script is headless
            browser_type="chromium"
        )
        
        print(f"\n✅ Headless search completed!")
        print(f"📊 Found {len(results)} results:")
        
        if results:
            for i, url in enumerate(results, 1):
                print(f"   {i}. {url}")
        else:
            print("   ⚠️  No results found - CAPTCHA may have blocked the search")
            
    except Exception as e:
        print(f"\n❌ Error during headless search: {e}")

async def test_search_from_url_headless_with_visible_captcha():
    """Test search from URL in headless mode with forced visible CAPTCHA."""
    print("\n\n🌐 Testing Search from URL (Headless with Visible CAPTCHA)")
    print("=" * 60)
    
    try:
        # Search from a specific Google URL that might trigger CAPTCHA
        google_url = "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024&start=0"
        results = await search_from_url(
            google_url, 
            provider="google", 
            max_results=3,
            headless=True,  # Main script is headless
            browser_type="chromium"
        )
        
        print(f"\n✅ URL search completed!")
        print(f"📊 Found {len(results)} results:")
        
        if results:
            for i, result in enumerate(results[:3], 1):
                url = result.get('url', 'N/A')
                title = result.get('title', 'N/A')
                print(f"   {i}. {url}")
                print(f"      Title: {title}")
        else:
            print("   ⚠️  No results found - CAPTCHA may have blocked the search")
            
    except Exception as e:
        print(f"\n❌ Error during URL search: {e}")

async def test_captcha_url_headless_with_visible():
    """Test with a direct CAPTCHA URL in headless mode."""
    print("\n\n🔐 Testing CAPTCHA URL (Headless with Visible Window)")
    print("=" * 55)
    
    try:
        # This is a CAPTCHA URL that should redirect to search results after solving
        captcha_url = "https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dtravel%2Bcard%2Bsite:pantip.com%2Bafter:2024%26as_epq%3Dtravel%2Bcard%26start%3D0&q=EhAkBZgAtlI6YO1Am8L6wQoRGMnhmMUGIjBEsfFR3J6tv2xAX9dwIPA2aCdGo0h4z34BraY2d0cAd54wyw78U3yynnTnc2_7zdgyAnJSWgFD"
        
        print("   🔗 Testing with CAPTCHA URL in headless mode...")
        print("   💡 Browser window should become visible for CAPTCHA solving")
        
        results = await search_from_url(
            captcha_url, 
            provider="google", 
            max_results=2,
            headless=True,  # Main script is headless
            browser_type="chromium"
        )
        
        print(f"\n✅ CAPTCHA URL search completed!")
        print(f"📊 Found {len(results)} results:")
        
        if results:
            for i, result in enumerate(results, 1):
                url = result.get('url', 'N/A')
                print(f"   {i}. {url}")
        else:
            print("   ⚠️  No results found after CAPTCHA solving")
            
    except Exception as e:
        print(f"\n❌ Error during CAPTCHA URL search: {e}")

def main():
    """Main function to run the forced visible CAPTCHA tests."""
    print("🎯 Forced Visible Window for CAPTCHA Solving Test")
    print("=" * 60)
    
    print("\n💡 Key Features:")
    print("   ✅ Main script runs in headless mode")
    print("   ✅ CAPTCHA detection forces visible window")
    print("   ✅ Manual CAPTCHA solving possible")
    print("   ✅ Same timeout as non-headless mode (5 minutes)")
    print("   ✅ Automatic detection when CAPTCHA is solved")
    
    print("\n🔧 Technical Details:")
    print("   - CrawlerRunConfig forces headless=False for CAPTCHA")
    print("   - Uses wait_for selectors to detect completion")
    print("   - Re-runs search with proper extraction after solving")
    print("   - Maintains headless performance for non-CAPTCHA cases")
    
    print("\n⚠️  Important Notes:")
    print("   - This test may trigger a real CAPTCHA challenge")
    print("   - Browser window will become visible when CAPTCHA is detected")
    print("   - You can solve CAPTCHA manually in the visible window")
    print("   - Script will continue automatically after solving")
    
    # Run the tests
    asyncio.run(test_headless_with_visible_captcha())
    asyncio.run(test_search_from_url_headless_with_visible_captcha())
    asyncio.run(test_captcha_url_headless_with_visible())
    
    print("\n\n🎉 Forced visible CAPTCHA test completed!")
    print("\n📝 What you should have experienced:")
    print("   ✅ Main script ran in headless mode")
    print("   ✅ Browser window became visible when CAPTCHA detected")
    print("   ✅ Manual CAPTCHA solving was possible")
    print("   ✅ Script continued automatically after solving")
    print("   💡 Best of both worlds: headless performance + manual CAPTCHA solving")

if __name__ == "__main__":
    main()

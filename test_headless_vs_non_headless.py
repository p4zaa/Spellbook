#!/usr/bin/env python3
"""
Test script to demonstrate the difference between headless and non-headless CAPTCHA handling.
This script shows how CAPTCHA is handled differently in each mode.
"""

import asyncio
from spellbook.scraper.search import search_google, search_from_url

async def test_headless_mode():
    """Test CAPTCHA handling in headless mode."""
    print("🔍 Testing CAPTCHA Handling in Headless Mode")
    print("=" * 50)
    
    print("\n📋 What this test does:")
    print("1. Opens a headless browser (no visible window)")
    print("2. Performs a Google search that might trigger CAPTCHA")
    print("3. If CAPTCHA is detected:")
    print("   - No browser window is visible")
    print("   - Script waits for automatic CAPTCHA solving")
    print("   - Shorter timeout (60 seconds)")
    print("   - Suggests using non-headless mode if needed")
    print("4. If no CAPTCHA, continues normally")
    
    print("\n🚀 Starting Google search in headless mode...")
    print("   ⚠️  This test may trigger a real CAPTCHA challenge")
    print("   💡 In headless mode, CAPTCHA solving may not work")
    
    try:
        # Perform a Google search with headless=True
        results = await search_google(
            "travel card site:pantip.com after:2024", 
            max_results=3,
            headless=True,  # Headless mode - no visible browser
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

async def test_non_headless_mode():
    """Test CAPTCHA handling in non-headless mode."""
    print("\n\n🌐 Testing CAPTCHA Handling in Non-Headless Mode")
    print("=" * 55)
    
    print("\n📋 What this test does:")
    print("1. Opens a visible browser window")
    print("2. Performs a Google search that might trigger CAPTCHA")
    print("3. If CAPTCHA is detected:")
    print("   - Browser window stays open and visible")
    print("   - You can solve the CAPTCHA manually")
    print("   - Longer timeout (5 minutes)")
    print("   - Automatic detection when solved")
    print("4. If no CAPTCHA, continues normally")
    
    print("\n🚀 Starting Google search in non-headless mode...")
    print("   ⚠️  This test may trigger a real CAPTCHA challenge")
    print("   💡 Browser window will be visible for manual CAPTCHA solving")
    
    try:
        # Perform a Google search with headless=False
        results = await search_google(
            "travel card site:pantip.com after:2024", 
            max_results=3,
            headless=False,  # Non-headless mode - visible browser
            browser_type="chromium"
        )
        
        print(f"\n✅ Non-headless search completed!")
        print(f"📊 Found {len(results)} results:")
        
        if results:
            for i, url in enumerate(results, 1):
                print(f"   {i}. {url}")
        else:
            print("   ⚠️  No results found - CAPTCHA may have blocked the search")
            
    except Exception as e:
        print(f"\n❌ Error during non-headless search: {e}")

async def test_captcha_url_comparison():
    """Test both modes with a direct CAPTCHA URL."""
    print("\n\n🔐 Testing CAPTCHA URL in Both Modes")
    print("=" * 40)
    
    captcha_url = "https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dtravel%2Bcard%2Bsite:pantip.com%2Bafter:2024%26as_epq%3Dtravel%2Bcard%26start%3D0&q=EhAkBZgAtlI6YO1Am8L6wQoRGMnhmMUGIjBEsfFR3J6tv2xAX9dwIPA2aCdGo0h4z34BraY2d0cAd54wyw78U3yynnTnc2_7zdgyAnJSWgFD"
    
    print("\n🔗 Testing with CAPTCHA URL...")
    print("   💡 This URL should trigger CAPTCHA in both modes")
    
    # Test headless mode
    print("\n1. Testing Headless Mode:")
    try:
        results_headless = await search_from_url(
            captcha_url, 
            provider="google", 
            max_results=2,
            headless=True,
            browser_type="chromium"
        )
        print(f"   📊 Headless results: {len(results_headless)} found")
    except Exception as e:
        print(f"   ❌ Headless error: {e}")
    
    # Test non-headless mode
    print("\n2. Testing Non-Headless Mode:")
    try:
        results_non_headless = await search_from_url(
            captcha_url, 
            provider="google", 
            max_results=2,
            headless=False,
            browser_type="chromium"
        )
        print(f"   📊 Non-headless results: {len(results_non_headless)} found")
    except Exception as e:
        print(f"   ❌ Non-headless error: {e}")

def main():
    """Main function to run the headless vs non-headless tests."""
    print("🎯 Headless vs Non-Headless CAPTCHA Handling Test")
    print("=" * 60)
    
    print("\n💡 Key Differences:")
    print("   🔍 Headless Mode:")
    print("      - No visible browser window")
    print("      - Shorter timeout (60 seconds)")
    print("      - May not work with CAPTCHA")
    print("      - Good for automated scripts")
    print("   🌐 Non-Headless Mode:")
    print("      - Visible browser window")
    print("      - Longer timeout (5 minutes)")
    print("      - Manual CAPTCHA solving possible")
    print("      - Better for interactive use")
    
    print("\n⚠️  Important Notes:")
    print("   - Headless mode may not work with CAPTCHA")
    print("   - Non-headless mode allows manual CAPTCHA solving")
    print("   - Both modes use the same wait_for detection")
    print("   - Choose mode based on your use case")
    
    # Run the tests
    asyncio.run(test_headless_mode())
    asyncio.run(test_non_headless_mode())
    asyncio.run(test_captcha_url_comparison())
    
    print("\n\n🎉 Headless vs non-headless test completed!")
    print("\n📝 Summary:")
    print("   ✅ Headless mode: No popup, shorter timeout")
    print("   ✅ Non-headless mode: Visible window, manual solving")
    print("   ✅ Both modes: Automatic detection when possible")
    print("   💡 Recommendation: Use non-headless for CAPTCHA-heavy sites")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for CAPTCHA solving and data extraction.
This script tests that after solving CAPTCHA, the search results are properly extracted.
"""

import asyncio
from spellbook.scraper.search import search_google, search_from_url

async def test_captcha_data_extraction():
    """Test that data is properly extracted after CAPTCHA solving."""
    print("🔍 Testing CAPTCHA Solving and Data Extraction")
    print("=" * 55)
    
    print("\n📋 What this test does:")
    print("1. Opens a visible browser window (headless=False)")
    print("2. Performs a Google search that might trigger CAPTCHA")
    print("3. If CAPTCHA is detected:")
    print("   - Browser window stays open")
    print("   - Waits for CAPTCHA to be solved")
    print("   - Re-runs search with proper extraction config")
    print("   - Extracts and displays search results")
    print("4. If no CAPTCHA, extracts results normally")
    
    print("\n🚀 Starting Google search with data extraction test...")
    print("   ⚠️  This test may trigger a real CAPTCHA challenge")
    print("   💡 After solving CAPTCHA, results should be extracted automatically")
    
    try:
        # Perform a Google search with headless=False
        results = await search_google(
            "travel card site:pantip.com after:2024", 
            max_results=5,
            headless=False,  # This opens a visible browser window
            browser_type="chromium"
        )
        
        print(f"\n✅ Search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        if results:
            for i, url in enumerate(results, 1):
                print(f"   {i}. {url}")
        else:
            print("   ⚠️  No results found - this might indicate an issue with extraction")
            
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("   This might be due to network issues or rate limiting.")

async def test_search_from_url_data_extraction():
    """Test search from URL with data extraction after CAPTCHA."""
    print("\n\n🌐 Testing Search from URL (Data Extraction)")
    print("=" * 45)
    
    try:
        # Search from a specific Google URL that might trigger CAPTCHA
        google_url = "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024&start=0"
        results = await search_from_url(
            google_url, 
            provider="google", 
            max_results=5,
            headless=False,  # Visible browser window
            browser_type="chromium"
        )
        
        print(f"\n✅ URL search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        if results:
            for i, result in enumerate(results[:5], 1):
                url = result.get('url', 'N/A')
                title = result.get('title', 'N/A')
                print(f"   {i}. {url}")
                print(f"      Title: {title}")
        else:
            print("   ⚠️  No results found - this might indicate an issue with extraction")
            
    except Exception as e:
        print(f"\n❌ Error during URL search: {e}")

async def test_captcha_url_direct():
    """Test with a direct CAPTCHA URL to ensure proper handling."""
    print("\n\n🔐 Testing Direct CAPTCHA URL Handling")
    print("=" * 45)
    
    try:
        # This is a CAPTCHA URL that should redirect to search results after solving
        captcha_url = "https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dtravel%2Bcard%2Bsite:pantip.com%2Bafter:2024%26as_epq%3Dtravel%2Bcard%26start%3D0&q=EhAkBZgAtlI6YO1Am8L6wQoRGMnhmMUGIjBEsfFR3J6tv2xAX9dwIPA2aCdGo0h4z34BraY2d0cAd54wyw78U3yynnTnc2_7zdgyAnJSWgFD"
        
        print("   🔗 Testing with CAPTCHA URL...")
        print("   💡 This should redirect to search results after CAPTCHA is solved")
        
        results = await search_from_url(
            captcha_url, 
            provider="google", 
            max_results=3,
            headless=False,
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
    """Main function to run the CAPTCHA data extraction tests."""
    print("🎯 CAPTCHA Solving and Data Extraction Test")
    print("=" * 50)
    
    print("\n💡 Key Features Being Tested:")
    print("   ✅ CAPTCHA detection and solving")
    print("   ✅ Automatic re-running of search after CAPTCHA")
    print("   ✅ Proper data extraction with original config")
    print("   ✅ Results display and validation")
    
    print("\n⚠️  Important Notes:")
    print("   - This test may trigger a real CAPTCHA challenge")
    print("   - The browser window should stay open for manual solving")
    print("   - After solving CAPTCHA, results should be extracted automatically")
    print("   - If no results are found, there may be an extraction issue")
    
    # Run the tests
    asyncio.run(test_captcha_data_extraction())
    asyncio.run(test_search_from_url_data_extraction())
    asyncio.run(test_captcha_url_direct())
    
    print("\n\n🎉 CAPTCHA data extraction test completed!")
    print("\n📝 What you should have experienced:")
    print("   ✅ Browser window opened and stayed visible")
    print("   ✅ CAPTCHA detection worked properly")
    print("   ✅ Script waited for CAPTCHA to be solved")
    print("   ✅ Search was re-run after CAPTCHA solving")
    print("   ✅ Results were extracted and displayed")

if __name__ == "__main__":
    main()

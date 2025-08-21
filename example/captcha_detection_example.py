#!/usr/bin/env python3
"""
Example demonstrating CAPTCHA detection in Google search functionality.

This script shows how the Spellbook scraper automatically detects when Google
presents a CAPTCHA challenge and handles it gracefully.
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import spellbook
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spellbook.scraper.search import search_google, search_keywords_all_platforms

async def demonstrate_captcha_detection():
    """Demonstrate CAPTCHA detection functionality."""
    print("🔍 Google Search with CAPTCHA Detection Demo")
    print("=" * 50)
    
    print("\n📋 What this demo does:")
    print("1. Performs Google searches using Spellbook's scraper")
    print("2. Automatically detects if Google shows a CAPTCHA (redirect URLs or HTML content)")
    print("3. If CAPTCHA is detected:")
    print("   - Prints a warning message with the redirect URL")
    print("   - Waits for you to solve it manually")
    print("   - Continues automatically after you press Enter")
    print("4. If no CAPTCHA, continues normally")
    
    print("\n🚀 Starting Google search...")
    
    try:
        # Perform a Google search
        results = await search_google("python programming tutorial", max_results=5)
        
        print(f"\n✅ Search completed successfully!")
        print(f"📊 Found {len(results)} results:")
        
        for i, url in enumerate(results, 1):
            print(f"   {i}. {url}")
            
    except Exception as e:
        print(f"\n❌ Error during search: {e}")
        print("   This might be due to network issues or rate limiting.")

async def demonstrate_multi_platform_search():
    """Demonstrate multi-platform search with CAPTCHA detection."""
    print("\n\n🌐 Multi-Platform Search Demo")
    print("=" * 40)
    
    keywords = ["python programming", "machine learning"]
    
    print(f"\n🔍 Searching for: {', '.join(keywords)}")
    print("📱 Platforms: Google, DuckDuckGo")
    
    try:
        results = await search_keywords_all_platforms(
            keywords=keywords,
            providers=["google", "duckduckgo"],
            max_results_per_provider=3,
            max_concurrent=2
        )
        
        print(f"\n✅ Multi-platform search completed!")
        print(f"📊 Found {len(results)} total results:")
        
        # Group results by platform
        by_platform = {}
        for result in results:
            platform = result.get("platform", "unknown")
            if platform not in by_platform:
                by_platform[platform] = []
            by_platform[platform].append(result.get("url"))
        
        for platform, urls in by_platform.items():
            print(f"\n   {platform.upper()}:")
            for i, url in enumerate(urls, 1):
                print(f"     {i}. {url}")
                
    except Exception as e:
        print(f"\n❌ Error during multi-platform search: {e}")

def main():
    """Main function to run the demo."""
    print("🎯 Spellbook CAPTCHA Detection Demo")
    print("=" * 50)
    
    print("\n💡 Note: This demo will automatically handle CAPTCHA challenges")
    print("   if Google presents them during the search process.")
    
    # Run the demos
    asyncio.run(demonstrate_captcha_detection())
    asyncio.run(demonstrate_multi_platform_search())
    
    print("\n\n🎉 Demo completed!")
    print("\n📝 Key Features Demonstrated:")
    print("   ✅ Automatic CAPTCHA detection")
    print("   ✅ Graceful handling of Google challenges")
    print("   ✅ Multi-platform search capabilities")
    print("   ✅ Error handling and user feedback")

if __name__ == "__main__":
    main()

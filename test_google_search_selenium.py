#!/usr/bin/env python3
"""
Test script for the Google search function using Selenium.
"""

from spellbook.scraper.google_search_basic import google_search_selenium, google_search_simple
import polars as pl

def test_google_search():
    """Test the Google search function with the example parameters."""
    
    print("🧪 Testing Google Search with Selenium")
    print("=" * 60)
    
    # Test parameters similar to the provided example
    keyword = 'เกาะพะงัน'
    site = 'twitter.com' #'pantip.com'
    year = 2024
    
    print(f"🔍 Search Parameters:")
    print(f"   Keyword: {keyword}")
    print(f"   Site: {site}")
    print(f"   Year: {year}")
    print(f"   Max Results: None (unlimited)")
    print(f"   Max Pages: 3")
    print(f"   Headless: False (you'll see the browser)")
    print(f"   Advanced CAPTCHA Detection: Enabled")
    print()
    
    try:
        # Test the full search function
        print("🚀 Starting Google search...")
        results = google_search_selenium(
            keyword=keyword,
            site=site,
            year=year,
            max_results=None,  # Get up to 10 results
            max_pages=1,     # Scrape up to 3 pages
            headless=False,  # Set to True if you don't want to see the browser
            wait_time=15
        )
        
        print(f"\n📊 Search Results ({len(results)} found):")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title'] or 'No title'}")
            print(f"   URL: {result['url'] or 'No URL'}")
            print(f"   Date: {result['date_string'] or 'No date'}")
            if result['related_content']:
                print(f"   Content: {result['related_content'][:150]}...")
            print()
        
        return results
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        print("💡 Make sure you have Chrome browser and ChromeDriver installed")


def test_different_queries():
    """Test with different search queries."""
    
    print("\n🧪 Testing Different Search Queries")
    print("=" * 60)
    
    test_cases = [
        {
            "keyword": "python selenium",
            "site": "stackoverflow.com",
            "year": 2024,
            "description": "Python Selenium questions on Stack Overflow"
        },
        {
            "keyword": "machine learning",
            "site": None,
            "year": 2024,
            "description": "General machine learning search"
        },
        {
            "keyword": "web scraping",
            "site": "github.com",
            "year": None,
            "description": "Web scraping projects on GitHub"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {test_case['description']}")
        print(f"   Keyword: {test_case['keyword']}")
        print(f"   Site: {test_case['site'] or 'Any site'}")
        print(f"   Year: {test_case['year'] or 'Any year'}")
        
        try:
            results = google_search_selenium(
                keyword=test_case['keyword'],
                site=test_case['site'],
                year=test_case['year'],
                max_results=3,
                headless=False,
                wait_time=10
            )
            
            print(f"   ✅ Found {len(results)} results")
            for j, result in enumerate(results, 1):
                print(f"      {j}. {result['title'][:60] if result['title'] else 'No title'}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    # Run the main test
    results = test_google_search()
    #print(results)
    #df = pl.DataFrame(results)
    #df.write_csv("google_search_results.csv")

    
    
    # Uncomment the line below to test different queries
    #test_different_queries()
    
    print("\n✅ Test completed!")

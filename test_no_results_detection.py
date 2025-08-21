#!/usr/bin/env python3
"""
Test script to demonstrate no results detection functionality.
Tests the detection of #botstuff > div > div.mnr-c selector and other no results indicators.
"""

import asyncio
import time
from spellbook.scraper.search import search_google, search_from_url
from spellbook.scraper.captcha_detector import detect_no_results


def test_no_results_detection():
    """Test the no results detection with sample HTML content."""
    print("🔍 Testing No Results Detection")
    print("=" * 40)
    
    # Test cases with different no results scenarios (using URLs instead of keywords)
    test_cases = [
        {
            "name": "Google No Results (CSS Selector #botstuff)",
            "url": "https://www.google.com/search?q=site:example.com+nonexistentkeyword",
            "html": '<div id="botstuff"><div><div class="mnr-c">No results found</div></div></div>',
            "domain": "google.com",
            "expected": True
        },
        {
            "name": "Google No Results (CSS Selector #OotqVd)",
            "url": "https://www.google.com/search?q=site:example.com+anothernonexistent",
            "html": '<div id="OotqVd">No results found for your search</div>',
            "domain": "google.com",
            "expected": True
        },
        {
            "name": "Google No Results (Text)",
            "url": "https://www.google.com/search?q=site:example.com+randomstringthatdoesnotexist",
            "html": '<div>Your search did not match any documents</div>',
            "domain": "google.com",
            "expected": True
        },
        {
            "name": "DuckDuckGo No Results",
            "url": "https://duckduckgo.com/?q=site:example.com+noresultshere",
            "html": '<div>No results found for your search</div>',
            "domain": "duckduckgo.com",
            "expected": True
        },
        {
            "name": "Pantip No Results (Thai)",
            "url": "https://pantip.com/search?q=ไม่มีผลลัพธ์",
            "html": '<div>ไม่พบผลลัพธ์</div>',
            "domain": "pantip.com",
            "expected": True
        },
        {
            "name": "Normal Results",
            "url": "https://www.google.com/search?q=site:example.com+somethingcommon",
            "html": '<div id="rso"><div class="g">Search result here</div></div>',
            "domain": "google.com",
            "expected": False
        },
        {
            "name": "Generic No Results",
            "url": "https://example.com/search?q=notfound",
            "html": '<div>No matches found for your query</div>',
            "domain": "example.com",
            "expected": True
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   URL: {test_case['url']}")
        print(f"   HTML: {test_case['html'][:50]}...")
        print(f"   Domain: {test_case['domain']}")
        
        has_no_results, no_results_type, details = detect_no_results(
            html_content=test_case['html'],
            domain=test_case['domain']
        )
        
        print(f"   Detected: {has_no_results}")
        print(f"   Type: {no_results_type}")
        print(f"   Details: {details}")
        print(f"   Expected: {test_case['expected']}")
        print(f"   Status: {'✅ PASS' if has_no_results == test_case['expected'] else '❌ FAIL'}")


async def test_google_no_results_search():
    """Test Google search with a URL that might return no results."""
    print("\n🔍 Testing Google Search with No Results Detection")
    print("=" * 55)
    
    # Try a very specific URL that might return no results
    test_urls = [
        "https://www.google.com/search?q=travel+card+site:pantip.com+after:2024+%22travel+card%22&start=310",
        # You can add more URLs that are likely to return no results
        # "https://www.google.com/search?q=site:example.com+randomstringofcharacters1234sg356465453153ew5"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing URL: '{url}'")
        start_time = time.time()
        
        try:
            results = await search_google(
                url,
                max_results=5,
                max_paginate=1,
                pagination_mode="multi_window",
                headless=False
            )
            
            elapsed = time.time() - start_time
            print(f"   ⏱️  Completed in {elapsed:.2f} seconds")
            print(f"   📊 Found {len(results)} results")
            
            if len(results) == 0:
                print("   ✅ No results detected - this is expected for this URL")
            else:
                print("   ⚠️  Found some results - URL might be too common")
                for i, url in enumerate(results[:2], 1):
                    print(f"      {i}. {url}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")


def explain_no_results_detection():
    """Explain how no results detection works."""
    print("\n📚 Understanding No Results Detection")
    print("=" * 45)
    
    print("\n🎯 Purpose:")
    print("   • Detect when search queries return no results")
    print("   • Avoid processing empty pages")
    print("   • Improve crawling efficiency")
    print("   • Provide better user feedback")
    
    print("\n🔍 Detection Methods:")
    print("   • CSS Selectors: #botstuff > div > div.mnr-c (Google)")
    print("   • Text Patterns: 'no results found', 'did not match'")
    print("   • Domain-specific indicators")
    print("   • Generic fallback patterns")
    
    print("\n🌐 Supported Domains:")
    print("   • Google: #botstuff > div > div.mnr-c, #OotqVd, 'did not match any documents'")
    print("   • DuckDuckGo: 'no results', 'no matches found'")
    print("   • Bing: 'no results', 'no matches found'")
    print("   • Pantip: 'ไม่พบผลลัพธ์', 'no results'")
    print("   • Generic: 'no results found', 'empty results'")
    
    print("\n⚡ Benefits:")
    print("   • Faster crawling (skip empty pages)")
    print("   • Better resource management")
    print("   • More accurate results")
    print("   • Improved user experience")


def show_detection_flow():
    """Show the no results detection flow."""
    print("\n🔄 No Results Detection Flow")
    print("=" * 35)
    
    steps = [
        "1. Load search page",
        "2. Extract HTML content",
        "3. Check for domain-specific selectors",
        "4. Check for text patterns",
        "5. Check for generic patterns",
        "6. If no results detected → Return empty list",
        "7. If results found → Continue with extraction",
        "8. Process search results normally"
    ]
    
    for step in steps:
        print(f"   {step}")
    
    print("\n🛡️ Safety Checks:")
    print("   • Multiple detection methods")
    print("   • Domain-specific patterns")
    print("   • Generic fallback patterns")
    print("   • Graceful handling")


def compare_detection_methods():
    """Compare different no results detection methods."""
    print("\n🔍 Detection Method Comparison")
    print("=" * 35)
    
    methods = [
        {
            "name": "CSS Selector Detection",
            "description": "Look for specific CSS selectors like #botstuff > div > div.mnr-c",
            "pros": ["Fast", "Reliable", "Domain-specific"],
            "cons": ["Requires selector knowledge", "May break with site updates"]
        },
        {
            "name": "Text Pattern Detection",
            "description": "Search for text patterns like 'no results found'",
            "pros": ["Language flexible", "Robust", "Easy to extend"],
            "cons": ["Slower", "May have false positives"]
        },
        {
            "name": "Combined Approach",
            "description": "Use both CSS selectors and text patterns",
            "pros": ["Most reliable", "Comprehensive", "Best coverage"],
            "cons": ["More complex", "Higher overhead"]
        }
    ]
    
    for i, method in enumerate(methods, 1):
        print(f"\n{i}. {method['name']}")
        print(f"   {method['description']}")
        print("   Pros:")
        for pro in method['pros']:
            print(f"      • {pro}")
        print("   Cons:")
        for con in method['cons']:
            print(f"      • {con}")


if __name__ == "__main__":
    print("🔍 No Results Detection Test Suite")
    print("This script tests the detection of no search results.")
    print()
    
    # Explain the functionality
    explain_no_results_detection()
    show_detection_flow()
    compare_detection_methods()
    
    print("\n" + "=" * 60)
    
    # Run tests
    print("\n🧪 Running Tests...")
    
    # Test detection logic
    test_no_results_detection()
    
    # Ask user if they want to test with real searches
    print("\n" + "=" * 60)
    choice = input("\nDo you want to test with real Google searches? (y/n): ").strip().lower()
    
    if choice == 'y':
        asyncio.run(test_google_no_results_search())
    else:
        print("Skipping real search tests.")
    
    print("\n✅ No results detection test completed!")

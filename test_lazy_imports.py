#!/usr/bin/env python3
"""
Test script to demonstrate lazy dependency loading in Spellbook.

This script shows that:
1. Importing spellbook doesn't install heavy dependencies
2. Dependencies are only loaded when you actually use the functionality
3. Helpful error messages guide you to install missing dependencies
"""

import sys
import time

def test_lazy_imports():
    print("Testing lazy dependency loading in Spellbook...")
    print("=" * 50)
    
    # Test 1: Basic import (should work without heavy dependencies)
    print("\n1. Testing basic import...")
    start_time = time.time()
    
    try:
        import spellbook
        import_time = time.time() - start_time
        print(f"✅ Successfully imported spellbook in {import_time:.3f}s")
        print(f"   Version: {spellbook.__version__}")
        print(f"   Author: {spellbook.__author__}")
    except ImportError as e:
        print(f"❌ Failed to import spellbook: {e}")
        return
    
    # Test 2: Access core functionality (should work with minimal dependencies)
    print("\n2. Testing core functionality...")
    try:
        # This should work with just polars, numpy, scikit-learn
        from spellbook.data import flatten_dataframe
        print("✅ Core data functionality accessible")
    except ImportError as e:
        print(f"❌ Core functionality failed: {e}")
    
    # Test 3: Try to access visualization (should fail gracefully if matplotlib not installed)
    print("\n3. Testing visualization module...")
    try:
        # This will trigger the lazy import and fail if matplotlib/wordcloud not installed
        from spellbook.viz import plot_wordcloud
        print("✅ Visualization module accessible (dependencies installed)")
    except ImportError as e:
        print(f"⚠️  Visualization module not available: {e}")
        print("   This is expected if you haven't installed: pip install -e .[viz]")
    
    # Test 4: Try to access text processing (should fail gracefully if pythainlp/nltk not installed)
    print("\n4. Testing text processing module...")
    try:
        from spellbook.text import tokenize_text
        print("✅ Text processing module accessible (dependencies installed)")
    except ImportError as e:
        print(f"⚠️  Text processing module not available: {e}")
        print("   This is expected if you haven't installed: pip install -e .[text]")
    
    # Test 5: Try to access web scraping (should fail gracefully if selenium not installed)
    print("\n5. Testing web scraping module...")
    try:
        from spellbook.scraper import google_search_basic
        print("✅ Web scraping module accessible (dependencies installed)")
    except ImportError as e:
        print(f"⚠️  Web scraping module not available: {e}")
        print("   This is expected if you haven't installed: pip install -e .[scraping]")
    
    print("\n" + "=" * 50)
    print("Lazy import test completed!")
    print("\nTo install specific functionality, use:")
    print("  pip install -e .[viz]      # For visualization")
    print("  pip install -e .[text]     # For text processing")
    print("  pip install -e .[scraping] # For web scraping")
    print("  pip install -e .[full]     # For all features")

if __name__ == "__main__":
    test_lazy_imports()

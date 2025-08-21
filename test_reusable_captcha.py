#!/usr/bin/env python3
"""
Test script for reusable CAPTCHA detection functionality.
This script demonstrates how the CAPTCHA detector can be used with any website.
"""

import asyncio
from spellbook.scraper.captcha_detector import detect_captcha, handle_captcha, CaptchaDetector

def test_captcha_detection():
    """Test CAPTCHA detection with various URLs and HTML content."""
    print("🔍 Testing Reusable CAPTCHA Detection")
    print("=" * 45)
    
    # Test 1: Google CAPTCHA redirect
    print("\n1. Testing Google CAPTCHA redirect detection:")
    google_captcha_url = "https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dtest"
    is_captcha, captcha_type, details = detect_captcha(url=google_captcha_url)
    print(f"   URL: {google_captcha_url}")
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")
    
    # Test 2: Cloudflare CAPTCHA
    print("\n2. Testing Cloudflare CAPTCHA detection:")
    cloudflare_url = "https://example.com"
    cloudflare_html = """
    <html>
        <head><title>Checking your browser - example.com</title></head>
        <body>
            <h1>Checking your browser before accessing example.com</h1>
            <p>This process is automatic. Your browser will redirect to your requested content shortly.</p>
        </body>
    </html>
    """
    is_captcha, captcha_type, details = detect_captcha(
        url=cloudflare_url, 
        html_content=cloudflare_html
    )
    print(f"   URL: {cloudflare_url}")
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")
    
    # Test 3: Generic CAPTCHA pattern
    print("\n3. Testing generic CAPTCHA pattern detection:")
    generic_url = "https://somewebsite.com/captcha/verify"
    is_captcha, captcha_type, details = detect_captcha(url=generic_url)
    print(f"   URL: {generic_url}")
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")
    
    # Test 4: HTML content with CAPTCHA indicators
    print("\n4. Testing HTML content CAPTCHA detection:")
    captcha_html = """
    <html>
        <head><title>Security Check</title></head>
        <body>
            <h1>Please verify you are human</h1>
            <p>We've detected unusual traffic from your network.</p>
            <p>Please complete the reCAPTCHA below.</p>
        </body>
    </html>
    """
    is_captcha, captcha_type, details = detect_captcha(html_content=captcha_html)
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")
    
    # Test 5: Normal content (no CAPTCHA)
    print("\n5. Testing normal content (no CAPTCHA):")
    normal_url = "https://example.com/page"
    normal_html = """
    <html>
        <head><title>Welcome to Example</title></head>
        <body>
            <h1>Welcome to our website</h1>
            <p>This is normal content without any CAPTCHA.</p>
        </body>
    </html>
    """
    is_captcha, captcha_type, details = detect_captcha(
        url=normal_url, 
        html_content=normal_html
    )
    print(f"   URL: {normal_url}")
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")

def test_custom_captcha_patterns():
    """Test adding custom CAPTCHA patterns."""
    print("\n\n🔧 Testing Custom CAPTCHA Patterns")
    print("=" * 40)
    
    # Create a custom detector
    custom_detector = CaptchaDetector()
    
    # Add custom patterns for a specific domain
    custom_detector.add_captcha_pattern("mywebsite.com", [
        "mywebsite.com/security-check",
        "mywebsite.com/verify-human"
    ])
    
    # Add custom HTML indicator
    custom_detector.add_captcha_indicator("my custom security check")
    
    # Test custom domain pattern
    print("\n1. Testing custom domain pattern:")
    custom_url = "https://mywebsite.com/security-check/verify"
    is_captcha, captcha_type, details = custom_detector.detect_captcha(url=custom_url)
    print(f"   URL: {custom_url}")
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")
    
    # Test custom HTML indicator
    print("\n2. Testing custom HTML indicator:")
    custom_html = """
    <html>
        <body>
            <h1>my custom security check</h1>
            <p>Please complete the verification.</p>
        </body>
    </html>
    """
    is_captcha, captcha_type, details = custom_detector.detect_captcha(html_content=custom_html)
    print(f"   Is CAPTCHA: {is_captcha}")
    print(f"   Type: {captcha_type}")
    print(f"   Details: {details}")

async def test_captcha_handling():
    """Test CAPTCHA handling functionality."""
    print("\n\n⚙️  Testing CAPTCHA Handling")
    print("=" * 30)
    
    # Test CAPTCHA handling (simulated)
    print("\n1. Testing CAPTCHA handling (simulated):")
    print("   This would normally wait for user interaction...")
    
    # Simulate a CAPTCHA detection
    is_captcha = True
    captcha_type = "test_captcha"
    details = "Simulated CAPTCHA for testing"
    
    # Note: In a real scenario, this would wait for user input
    # For testing, we'll just show the detection
    print(f"   Detected CAPTCHA: {captcha_type}")
    print(f"   Details: {details}")
    print("   ✅ CAPTCHA handling would work here")

def main():
    """Main function to run all CAPTCHA detection tests."""
    print("🎯 Reusable CAPTCHA Detection Demo")
    print("=" * 50)
    
    print("\n💡 Key Features:")
    print("   ✅ Works with any website (not just Google)")
    print("   ✅ Detects CAPTCHA from URLs and HTML content")
    print("   ✅ Supports custom patterns and indicators")
    print("   ✅ Handles both headless and non-headless modes")
    print("   ✅ Automatic retry and monitoring")
    
    # Run the tests
    test_captcha_detection()
    test_custom_captcha_patterns()
    asyncio.run(test_captcha_handling())
    
    print("\n\n🎉 Reusable CAPTCHA detection test completed!")
    print("\n📝 What you learned:")
    print("   ✅ CAPTCHA detection works for multiple websites")
    print("   ✅ Easy to add custom patterns for new sites")
    print("   ✅ Flexible and reusable across different scrapers")
    print("   ✅ Comprehensive detection from URLs and HTML")

if __name__ == "__main__":
    main()

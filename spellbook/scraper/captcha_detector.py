"""
CAPTCHA Detection Module

This module provides reusable CAPTCHA detection functionality that can be used
with any website, not just Google. It includes detection for various CAPTCHA
types and redirect patterns.
"""

import asyncio
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse


class CaptchaDetector:
    """Reusable CAPTCHA detection for any website."""
    
    def __init__(self):
        # Common CAPTCHA indicators in HTML content
        self.captcha_indicators = [
            "unusual traffic",
            "automated requests",
            "captcha",
            "verify you are human",
            "robot check",
            "security check",
            "recaptcha",
            "cloudflare",
            "ddos protection",
            "rate limit",
            "too many requests",
            "please wait",
            "checking your browser",
            "human verification",
            "bot detection"
        ]
        
        # Common CAPTCHA redirect patterns by domain
        self.captcha_redirects = {
            "google.com": ["google.com/sorry", "google.com/recaptcha"],
            "cloudflare.com": ["cloudflare.com/challenge", "cloudflare.com/security"],
            "duckduckgo.com": ["duckduckgo.com/sorry", "duckduckgo.com/challenge"],
            "bing.com": ["bing.com/sorry", "bing.com/security"],
            "yahoo.com": ["yahoo.com/sorry", "yahoo.com/security"],
            "facebook.com": ["facebook.com/checkpoint", "facebook.com/sorry"],
            "twitter.com": ["twitter.com/sorry", "twitter.com/account/access"],
            "instagram.com": ["instagram.com/challenge", "instagram.com/sorry"],
            "linkedin.com": ["linkedin.com/sorry", "linkedin.com/security"],
            "reddit.com": ["reddit.com/sorry", "reddit.com/security"],
            "pantip.com": ["pantip.com/sorry", "pantip.com/security"],
        }
        
        # Generic CAPTCHA redirect patterns
        self.generic_captcha_patterns = [
            "/sorry",
            "/captcha",
            "/challenge",
            "/security",
            "/verify",
            "/checkpoint",
            "/recaptcha",
            "/human-verification",
            "/bot-detection"
        ]

    def detect_captcha_from_url(self, url: str) -> Tuple[bool, str, str]:
        """
        Detect CAPTCHA from URL patterns.
        
        Args:
            url: The URL to check for CAPTCHA patterns
            
        Returns:
            Tuple of (is_captcha, captcha_type, details)
        """
        if not url:
            return False, "", ""
            
        url_lower = url.lower()
        parsed = urlparse(url)
        domain = parsed.hostname or ""
        
        # Check domain-specific CAPTCHA redirects
        for check_domain, patterns in self.captcha_redirects.items():
            if check_domain in domain:
                for pattern in patterns:
                    if pattern in url_lower:
                        return True, f"{check_domain}_redirect", f"Redirect to {url}"
        
        # Check generic CAPTCHA patterns
        for pattern in self.generic_captcha_patterns:
            if pattern in url_lower:
                return True, "generic_redirect", f"Generic CAPTCHA redirect: {url}"
        
        return False, "", ""

    def detect_captcha_from_html(self, html_content: str) -> Tuple[bool, str, str]:
        """
        Detect CAPTCHA from HTML content.
        
        Args:
            html_content: The HTML content to check for CAPTCHA indicators
            
        Returns:
            Tuple of (is_captcha, captcha_type, details)
        """
        if not html_content:
            return False, "", ""
            
        html_lower = html_content.lower()
        
        # Check for CAPTCHA indicators
        found_indicators = []
        for indicator in self.captcha_indicators:
            if indicator in html_lower:
                found_indicators.append(indicator)
        
        if found_indicators:
            return True, "html_content", f"Found indicators: {', '.join(found_indicators)}"
        
        return False, "", ""

    def detect_captcha(self, url: str = "", html_content: str = "", domain: str = "") -> Tuple[bool, str, str]:
        """
        Comprehensive CAPTCHA detection from URL and/or HTML content.
        
        Args:
            url: The URL to check for CAPTCHA patterns
            html_content: The HTML content to check for CAPTCHA indicators
            domain: Optional domain hint for better detection
            
        Returns:
            Tuple of (is_captcha, captcha_type, details)
        """
        # Check URL first
        if url:
            is_captcha, captcha_type, details = self.detect_captcha_from_url(url)
            if is_captcha:
                return True, captcha_type, details
        
        # Check HTML content
        if html_content:
            is_captcha, captcha_type, details = self.detect_captcha_from_html(html_content)
            if is_captcha:
                return True, captcha_type, details
        
        return False, "", ""

    async def handle_captcha(
        self, 
        is_captcha: bool, 
        captcha_type: str, 
        details: str, 
        url: str = "",
        headless: bool = True,
        max_wait_time: int = 300,
        crawler=None,
        retry_url: str = "",
        retry_config=None
    ) -> bool:
        """
        Handle CAPTCHA detection with appropriate user interaction.
        
        Args:
            is_captcha: Whether CAPTCHA was detected
            captcha_type: Type of CAPTCHA detected
            details: Details about the CAPTCHA
            url: Original URL that triggered CAPTCHA
            headless: Whether running in headless mode
            max_wait_time: Maximum time to wait for CAPTCHA solving (seconds)
            crawler: Crawler instance for retry attempts
            retry_url: URL to retry after CAPTCHA solving
            retry_config: Config to use for retry attempts
            
        Returns:
            True if CAPTCHA was handled successfully, False otherwise
        """
        if not is_captcha:
            return True
        
        print(f"⚠️  CAPTCHA detected: {captcha_type}")
        print(f"   Details: {details}")
        if url:
            print(f"   URL: {url}")
        
        if headless:
            print("   ⏳ Waiting for manual intervention...")
            try:
                input("Press Enter after solving the CAPTCHA to continue...")
                print("Continuing with search...")
                return True
            except KeyboardInterrupt:
                print("   ❌ CAPTCHA solving cancelled by user")
                return False
        else:
            print("   💡 Browser window is visible - solve the CAPTCHA there")
            print("   ⏳ Waiting for CAPTCHA to be solved...")
            print("   📝 After solving, the script will continue automatically")
            
            # Wait for CAPTCHA to be solved by monitoring the page
            wait_interval = 5  # Check every 5 seconds
            waited_time = 0
            
            while waited_time < max_wait_time:
                await asyncio.sleep(wait_interval)
                waited_time += wait_interval
                
                # Try to check if CAPTCHA is solved by making a small request
                if crawler and retry_url and retry_config:
                    try:
                        check_result = await crawler.arun(url=retry_url, config=retry_config)
                        if check_result and check_result.url:
                            # Check if we're no longer on a CAPTCHA page
                            is_still_captcha, _, _ = self.detect_captcha(
                                url=check_result.url, 
                                html_content=check_result.html or ""
                            )
                            if not is_still_captcha:
                                print("   ✅ CAPTCHA appears to be solved! Continuing...")
                                return True
                    except Exception:
                        pass
                
                if waited_time % 30 == 0:  # Print status every 30 seconds
                    print(f"   ⏰ Still waiting... ({waited_time}s elapsed)")
            
            print("   ⚠️  Timeout waiting for CAPTCHA. Continuing anyway...")
            return True

    def add_captcha_pattern(self, domain: str, patterns: List[str]):
        """
        Add custom CAPTCHA patterns for a specific domain.
        
        Args:
            domain: Domain to add patterns for
            patterns: List of URL patterns that indicate CAPTCHA
        """
        if domain not in self.captcha_redirects:
            self.captcha_redirects[domain] = []
        self.captcha_redirects[domain].extend(patterns)

    def add_captcha_indicator(self, indicator: str):
        """
        Add a custom CAPTCHA indicator for HTML content detection.
        
        Args:
            indicator: Text indicator to look for in HTML content
        """
        if indicator not in self.captcha_indicators:
            self.captcha_indicators.append(indicator)


# Global instance for easy use
captcha_detector = CaptchaDetector()


def detect_captcha(url: str = "", html_content: str = "", domain: str = "") -> Tuple[bool, str, str]:
    """
    Convenience function for CAPTCHA detection.
    
    Args:
        url: The URL to check for CAPTCHA patterns
        html_content: The HTML content to check for CAPTCHA indicators
        domain: Optional domain hint for better detection
        
    Returns:
        Tuple of (is_captcha, captcha_type, details)
    """
    return captcha_detector.detect_captcha(url, html_content, domain)


async def handle_captcha(
    is_captcha: bool, 
    captcha_type: str, 
    details: str, 
    url: str = "",
    headless: bool = True,
    max_wait_time: int = 300,
    crawler=None,
    retry_url: str = "",
    retry_config=None
) -> bool:
    """
    Convenience function for CAPTCHA handling.
    
    Args:
        is_captcha: Whether CAPTCHA was detected
        captcha_type: Type of CAPTCHA detected
        details: Details about the CAPTCHA
        url: Original URL that triggered CAPTCHA
        headless: Whether running in headless mode
        max_wait_time: Maximum time to wait for CAPTCHA solving (seconds)
        crawler: Crawler instance for retry attempts
        retry_url: URL to retry after CAPTCHA solving
        retry_config: Config to use for retry attempts
        
    Returns:
        True if CAPTCHA was handled successfully, False otherwise
    """
    return await captcha_detector.handle_captcha(
        is_captcha, captcha_type, details, url, headless, 
        max_wait_time, crawler, retry_url, retry_config
    )

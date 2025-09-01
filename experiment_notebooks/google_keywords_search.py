#!/usr/bin/env python3
"""
Google Keywords Search Script

This script performs Google searches for multiple keywords across multiple sites
using the Selenium-based Google search function. Results are returned as a dataframe.
"""

import sys
import os
import time
from typing import List, Dict, Any
import polars as pl

# Add the parent directory to the path to import spellbook modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spellbook.scraper.google_search_basic import google_search_selenium
from spellbook import utils as sb_utils


def get_keywords_and_sites():
    """Get the keywords and site lists for searching."""
    
    keywords = [
        #"travel card",
        #"บัตรเดบิต",
        "โมบายแบงก์กิ้ง",
        "กองทุน",
        "ประกันชีวิต",
        "ประกันภัย",
        "บัตรกดเงินสด",
        "บัตรเครดิต",
        "สินเชื่อรถ",
        "สินเชื่อบ้าน",
        "สินเชื่อส่วนบุคคล",
        "บัญชี",
    ]

    site_list = [
        'pantip.com',
        'x.com',
        'facebook.com',
        'tiktok.com',
        #'twitter.com',
        'instagram.com',
    ]
    
    return keywords, site_list


def search_keyword_site_combination(
    keyword: str,
    site: str,
    year: int = 2024,
    max_results: int = 20,
    max_pages: int = 3,
    headless: bool = False,
    wait_time: int = 10,
    captcha_max_wait_time: int = 1800
) -> List[Dict[str, Any]]:
    """
    Search for a specific keyword on a specific site.
    
    Args:
        keyword: Search keyword
        site: Site to search on
        year: Year filter (default: 2024)
        max_results: Maximum number of results
        max_pages: Maximum number of pages to scrape
        headless: Whether to run headless
        wait_time: Time to wait for page elements
        
    Returns:
        List of search results with additional metadata
    """
    
    print(f"🔍 Searching: '{keyword}' on {site} (year: {year})")
    
    try:
        # Perform the search
        results = google_search_selenium(
            keyword=keyword,
            site=site,
            year=year,
            max_results=max_results,
            max_pages=max_pages,
            headless=headless,
            wait_time=wait_time,
            captcha_max_wait_time=captcha_max_wait_time
        )
        
        # Add metadata to each result
        for result in results:
            result['keyword'] = keyword
            result['site'] = site
            result['search_year'] = year
            result['search_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"✅ Found {len(results)} results for '{keyword}' on {site}")
        return results
        
    except Exception as e:
        print(f"❌ Error searching '{keyword}' on {site}: {e}")
        return []


def search_all_combinations(
    keywords: List[str] = None,
    sites: List[str] = None,
    year: int = 2024,
    max_results: int = 20,
    max_pages: int = 3,
    headless: bool = False,
    wait_time: int = 10,
    delay_between_searches: int = 5,
    captcha_max_wait_time: int = 1800
) -> pl.DataFrame:
    """
    Search all keyword-site combinations and return results as a dataframe.
    
    Args:
        keywords: List of keywords to search (if None, uses default list)
        sites: List of sites to search (if None, uses default list)
        year: Year filter (default: 2024)
        max_results: Maximum number of results per search
        max_pages: Maximum number of pages per search
        headless: Whether to run headless
        wait_time: Time to wait for page elements
        delay_between_searches: Delay between searches in seconds
        
    Returns:
        Polars DataFrame with all search results
    """
    
    # Use default lists if not provided
    if keywords is None:
        keywords, _ = get_keywords_and_sites()
    if sites is None:
        _, sites = get_keywords_and_sites()
    
    print(f"🚀 Starting Google Keywords Search")
    print(f"📝 Keywords: {len(keywords)}")
    print(f"🌐 Sites: {len(sites)}")
    print(f"📅 Year: {year}")
    print(f"📊 Max Results per search: {max_results}")
    print(f"📄 Max Pages per search: {max_pages}")
    print(f"⏱️  Delay between searches: {delay_between_searches}s")
    print("=" * 60)
    
    all_results = []
    total_combinations = len(keywords) * len(sites)
    current_combination = 0
    
    for keyword in keywords:
        for site in sites:
            current_combination += 1
            print(f"\n📊 Progress: {current_combination}/{total_combinations}")
            
            # Search for this keyword-site combination
            results = search_keyword_site_combination(
                keyword=keyword,
                site=site,
                year=year,
                max_results=max_results,
                max_pages=max_pages,
                headless=headless,
                wait_time=wait_time,
                captcha_max_wait_time=captcha_max_wait_time
            )
            
            all_results.extend(results)
            
            # Save individual keyword-site results immediately
            if results:
                # Create keyword directory
                files_dir = os.path.join(os.path.dirname(__file__), '.files')
                keyword_dir = os.path.join(files_dir, keyword)
                os.makedirs(keyword_dir, exist_ok=True)
                
                # Create filename: keyword_site_after_year.csv
                clean_keyword = keyword.replace(' ', '_').replace('/', '_').replace('\\', '_')
                clean_site = site.replace('.', '_')
                filename = f"{clean_keyword}_{clean_site}_after_{year}.csv"
                filepath = os.path.join(keyword_dir, filename)
                
                try:
                    # Convert results to DataFrame and save
                    results_df = pl.DataFrame(results)
                    results_df.write_csv(filepath)
                    print(f"💾 Saved: {len(results)} results → {filepath}")
                except Exception as e:
                    print(f"❌ Error saving {keyword} - {site}: {e}")
            
            # Add delay between searches to avoid rate limiting
            if current_combination < total_combinations:
                print(f"⏳ Waiting {delay_between_searches} seconds before next search...")
                time.sleep(delay_between_searches)
    
    print(f"\n✅ Search completed!")
    print(f"📊 Total results collected: {len(all_results)}")
    
    # Convert to DataFrame
    if all_results:
        df = pl.DataFrame(all_results)
        
        # Add additional processing columns
        df = df.with_columns([
            # Parse Thai dates if available
            pl.col('date_string').map_elements(
                lambda s: sb_utils.datetime_processing.parse_thai_date(s) if s else None, 
                return_dtype=pl.Date
            ).alias("parsed_date"),
            
            # Create unique ID from URL
            pl.col('url').map_elements(
                lambda u: sb_utils.hashing.hash_function(u.strip(), algo='md5') if u else None, 
                return_dtype=pl.Utf8
            ).alias("id")
        ])
        
        return df
    else:
        # Return empty DataFrame with expected schema
        return pl.DataFrame({
            'url': [],
            'title': [],
            'related_content': [],
            'date_string': [],
            'keyword': [],
            'site': [],
            'search_year': [],
            'search_timestamp': [],
            'parsed_date': [],
            'id': []
        })


def save_results_to_excel(df: pl.DataFrame, filename: str = None):
    """
    Save results to Excel file.
    
    Args:
        df: DataFrame to save
        filename: Output filename (if None, uses default)
    """
    
    if filename is None:
        filename = "google_keywords_search_results.xlsx"
    
    # Ensure the .files directory exists
    files_dir = os.path.join(os.path.dirname(__file__), '.files')
    os.makedirs(files_dir, exist_ok=True)
    
    filepath = os.path.join(files_dir, filename)
    
    try:
        df.write_excel(filepath)
        print(f"💾 Results saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving to Excel: {e}")
        return None


def save_results_to_csv(df: pl.DataFrame, filename: str = None):
    """
    Save results to CSV file.
    
    Args:
        df: DataFrame to save
        filename: Output filename (if None, uses default)
    """
    
    if filename is None:
        filename = "google_keywords_search_results.csv"
    
    # Ensure the .files directory exists
    files_dir = os.path.join(os.path.dirname(__file__), '.files')
    os.makedirs(files_dir, exist_ok=True)
    
    filepath = os.path.join(files_dir, filename)
    
    try:
        df.write_csv(filepath)
        print(f"💾 Results saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")
        return None


def main():
    """Main function to run the Google keywords search."""
    
    print("🔍 Google Keywords Search Script")
    print("=" * 50)
    
    # Get keywords and sites
    keywords, sites = get_keywords_and_sites()
    
    # Perform all searches
    df = search_all_combinations(
        keywords=keywords,
        sites=sites,
        year=2024,  # Fixed year as requested
        max_results=None,
        max_pages=40,
        headless=False,  # Set to True for production
        wait_time=15,
        delay_between_searches=10,
        captcha_max_wait_time=7200 # 2 hours
    )
    
    # Display summary
    print(f"\n📊 Search Summary:")
    print(f"   Total results: {len(df)}")
    print(f"   Unique keywords: {df['keyword'].n_unique()}")
    print(f"   Unique sites: {df['site'].n_unique()}")
    print(f"   Unique URLs: {df['url'].n_unique()}")
    
    # Show sample results
    if len(df) > 0:
        print(f"\n📋 Sample Results:")
        print(df.head(5).select(['keyword', 'site', 'title', 'url']))
    
    # Save results
    excel_file = save_results_to_excel(df, "P_Mo_2025_Keywords_Search.xlsx")
    csv_file = save_results_to_csv(df, "P_Mo_2025_Keywords_Search.csv")
    
    print(f"\n✅ Search completed successfully!")
    print(f"📁 Files saved:")
    if excel_file:
        print(f"   Excel: {excel_file}")
    if csv_file:
        print(f"   CSV: {csv_file}")
    print(f"   📂 Keyword directories: .files/{{keyword}}/")
    
    return df


if __name__ == "__main__":
    # Run the main function
    results_df = main()
    
    # You can also access the results programmatically
    # print(f"DataFrame shape: {results_df.shape}")
    # print(f"Columns: {results_df.columns}")

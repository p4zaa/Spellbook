import polars as pl
import asyncio
import sys

sys.path.append('/Users/pa/Local Documents/GitHub Repositories/Spellbook') #for macos
#sys.path.append(r'C:\Users\patom\OneDrive\Documents\Repo\Spellbook') # for windows

from spellbook import scraper, utils as sb_utils
from crawl4ai import AsyncWebCrawler, BrowserConfig
from spellbook.scraper.search import _google_extraction_config, _create_google_dispatcher

keywords = [
    "travel card",
    "บัตรเดบิต",
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
  'twitter.com',
  'instagram.com',
]

results_list = []

async def search_with_shared_browser(crawler, keyword, site):
    """Search using a shared browser instance."""
    keyword_mod = keyword.lower().replace(' ', '+')
    google_search_url = f"https://www.google.com/search?q={keyword_mod}+site:{site}+after:2024&as_epq={keyword_mod}"
    print(f'Crawling::{keyword_mod} Site::{site}\n{google_search_url}')

    # Create extraction config
    config = _google_extraction_config(max_paginate=1, pagination_mode="multi_window")
    
    # Create dispatcher
    dispatcher = _create_google_dispatcher(enable_monitoring=True)
    
    # Generate URLs for pagination
    per_page = 10
    pages = 30  # max_paginate
    urls_to_fetch = []
    
    for page in range(pages):
        start = page * per_page
        if "?" in google_search_url:
            url = f"{google_search_url}&start={start}"
        else:
            url = f"{google_search_url}?start={start}"
        urls_to_fetch.append(url)
    
    # Reverse order to start from last page
    urls_to_fetch.reverse()
    print(f"   🔄 Reversed URL order: starting from page {pages} (backward)")
    
    try:
        # Use arun_many with the shared crawler
        results = await crawler.arun_many(
            urls=urls_to_fetch,
            config=config,
            dispatcher=dispatcher
        )
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if result and result.extracted_content:
                try:
                    import json
                    page_data = json.loads(result.extracted_content)
                    
                    for item in page_data:
                        if isinstance(item, dict) and 'url' in item:
                            # Add metadata
                            item['site'] = site
                            item['keyword'] = keyword
                            processed_results.append(item)
                            
                except Exception as e:
                    print(f"   ❌ Error parsing page {i + 1}: {e}")
        
        print(f"   📊 Found {len(processed_results)} results for {keyword} on {site}")
        return processed_results
        
    except Exception as e:
        print(f"   ❌ Error during search: {e}")
        return []

async def main():
    # Initialize browser only once
    print("🚀 Initializing browser...")
    browser_config = BrowserConfig(browser_type="chromium", headless=False)
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        print("✅ Browser initialized successfully")
        
        for keyword in keywords:
            for site in site_list:
                results = await search_with_shared_browser(crawler, keyword, site)
                results_list.extend(results)
                
                # Save partial results after each site
                if results:
                    df = pl.DataFrame(results)
                    df = df.with_columns(
                        pl.col('date_string').map_elements(lambda s: sb_utils.datetime_processing.parse_thai_date(s), return_dtype=pl.Date).alias("parsed_date"),
                        pl.col('url').map_elements(lambda u: sb_utils.hashing.hash_function(u.strip(), algo='md5'), return_dtype=pl.Utf8).alias("id")
                    )
                    df.write_csv(f'/Users/pa/Local Documents/GitHub Repositories/Spellbook/experiment_notebooks/.files/parts/{keyword}_{site}.csv')
        
        print("🔚 Browser session completed")

    # Save final combined results
    if results_list:
        df = pl.DataFrame(results_list)
        df = df.with_columns(
            pl.col('date_string').map_elements(lambda s: sb_utils.datetime_processing.parse_thai_date(s), return_dtype=pl.Date).alias("parsed_date"),
            pl.col('url').map_elements(lambda u: sb_utils.hashing.hash_function(u.strip(), algo='md5'), return_dtype=pl.Utf8).alias("id")
        )
        df.write_excel('/Users/pa/Local Documents/GitHub Repositories/Spellbook/experiment_notebooks/.files/P_Mo_2025_Keywords_Search.xlsx')
        print(f"💾 Final results saved to Excel file")

if __name__ == "__main__":
    asyncio.run(main())
    print(f"\nTotal results collected: {len(results_list)}")


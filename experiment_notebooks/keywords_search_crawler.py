import polars as pl
import asyncio
import sys

sys.path.append('/Users/pa/Local Documents/GitHub Repositories/Spellbook') #for macos
#sys.path.append(r'C:\Users\patom\OneDrive\Documents\Repo\Spellbook') # for windows

from spellbook import scraper, utils as sb_utils

keywords = [
    "travel card",
    #"บัตรเดบิต",
    #"โมบายแบงก์กิ้ง",
    #"กองทุน",
    #"ประกันชีวิต",
    #"ประกันภัย",
    #"บัตรกดเงินสด",
    #"บัตรเครดิต",
    #"สินเชื่อรถ",
    #"สินเชื่อบ้าน",
    #"สินเชื่อส่วนบุคคล",
    #"บัญชี",
    ]

site_list = [
  'pantip.com',
  #'x.com',
  #'facebook.com',
  #'tiktok.com',
  #'twitter.com',
  #'instagram.com',
]

results_list = []

async def main():
    for keyword in keywords:
        for site in site_list:
            keyword_mod = keyword.lower().replace(' ', '+')
            google_search_url = f"https://www.google.com/search?q={keyword_mod}+site:{site}+after:2024&as_epq={keyword_mod}"
            print(f'Crawling::{keyword_mod} Site::{site}\n{google_search_url}')

            results = await scraper.search.search_from_url(
                google_search_url,
                provider="google",
                max_results=None,
                return_schema=True,
                max_paginate=3,
                headless=False,
                pagination_mode='multi_window',
            )

            # Add 'site' and 'keyword' to each result dict
            for r in results:
                r['site'] = site
                r['keyword'] = keyword
            results_list.extend(results)

    df = pl.DataFrame(results_list)
    df = df.with_columns(
        pl.col('date_string').map_elements(lambda s: sb_utils.datetime_processing.parse_thai_date(s), return_dtype=pl.Date).alias("parsed_date"),
        pl.col('url').map_elements(lambda u: sb_utils.hashing.hash_function(u.strip(), algo='md5'), return_dtype=pl.Utf8).alias("id")
    )
    df.write_excel(r'.files\P_Mo_2025_Keywords_Search.xlsx')

if __name__ == "__main__":
    asyncio.run(main())
    print(f"\nTotal results collected: {len(results_list)}")


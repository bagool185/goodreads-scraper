import urllib.parse
from typing import List, Optional

from helpers.http_util import HttpUtil
from models.BookSelection import BookSelection, BookSelectionList
from bs4 import BeautifulSoup as BSoup

# presumably speeds up scraping
import cchardet


class SearchPageLocators:
    TABLE_LIST = '.tableList'
    TOP_RESULTS = 'tr'
    BOOK_TITLE = '.bookTitle'


class SearchPage:

    def __init__(self, base_url: str):
        self.url = f'{base_url}/search?query='

    async def get_top_results_async(self, search_term: str, max_results: Optional[int]) -> BookSelectionList:

        max_results = max_results if max_results else 5

        sanitised_search_term: str = urllib.parse.quote(search_term)

        page_content: BSoup = await HttpUtil.bsoup_from_url_async(self.url + sanitised_search_term)
        top_results: List[BSoup] = page_content.select(SearchPageLocators.TOP_RESULTS, limit=max_results)
        scraped_results: List[BookSelection] = []

        for result in top_results:
            url_obj: BSoup = result.select_one(SearchPageLocators.BOOK_TITLE)
            stripped_url: str = f'www.goodreads.com{url_obj["href"]}'.split('?')[0]
            search_result: BookSelection = BookSelection(title=url_obj.text.strip('\t\r\n'), url=stripped_url)
            scraped_results.append(search_result)

        return BookSelectionList(__root__=scraped_results)

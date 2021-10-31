import urllib.parse
from typing import List

from helpers.http_util import HttpUtil
from models.BookSelection import BookSelection
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

    async def get_top_results_async(self, search_term: str, max_results: int = 5) -> List[BookSelection]:
        sanitised_search_term: str = urllib.parse.quote(search_term)

        page_content: BSoup = await HttpUtil.bsoup_from_url_async(self.url + sanitised_search_term)
        top_results: List[BSoup] = page_content.select(SearchPageLocators.TOP_RESULTS, limit=max_results)
        scraped_results: List[BookSelection] = []

        for result in top_results:
            url_obj: BSoup = result.select_one(SearchPageLocators.BOOK_TITLE)

            search_result: BookSelection = BookSelection(title=url_obj.text.strip('\t\r\n'), url=url_obj['href'])
            scraped_results.append(search_result)

        return scraped_results

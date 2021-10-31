from typing import List

from models.BookSelection import BookSelection, BookSelectionDetails
from pages.book_page import BookPage
from pages.search_page import SearchPage


class GoodreadsService:
    def __init__(self):
        # TODO - get from environment?
        self.base_url: str = 'https://www.goodreads.com'
        self.search_page: SearchPage = SearchPage(self.base_url)
        self.book_page: BookPage = BookPage(self.base_url)

    async def search_async(self, search_term: str) -> List[BookSelection]:
        return await self.search_page.get_top_results_async(search_term)

    async def parse_detailed_book_view_async(self, book_selection: BookSelection) -> BookSelectionDetails:
        return await self.book_page.parse_detailed_book_view_async(book_selection)

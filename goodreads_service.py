import urllib.parse
from typing import List, Optional

import aiohttp
from bs4 import BeautifulSoup as BSoup, ResultSet
from pydantic import BaseModel


# TODO - move to designated models directory
class BookEntry(BaseModel):
    url: Optional[str]
    title: Optional[str]


class BookSelectionDetails(BaseModel):
    description: str
    cover_image_url: str
    title: str
    series: Optional[str]
    authors: List[str]
    genres: List[str]
    related_books: List[BookEntry]
    rating: str
    pages: str


class GoodreadsService:
    def __init__(self):
        # TODO - get from environment?
        self.base_url: str = 'https://www.goodreads.com'

    # TODO -move to its own helper or summat
    async def _bsoup_from_url_async(self, url: str) -> BSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return BSoup(await response.text(), 'html.parser')

    async def search_async(self, search_term: str) -> List[BookEntry]:
        # TODO - add caching
        sanitised_url: str = urllib.parse.quote(search_term)
        endpoint = f'{self.base_url}/search?query={sanitised_url}'

        page_content: BSoup = await self._bsoup_from_url_async(endpoint)
        table_list: BSoup = page_content.find('table', class_='tableList')
        # TODO - use a page pattern & make it faster
        if table_list is not None:
            top_results: ResultSet = table_list.find_all('tr', limit=5)
            scraped_results: List[BookEntry] = []

            for result in top_results:

                url_obj: BSoup = result.find('a', class_='bookTitle')

                search_result: BookEntry = BookEntry(title=url_obj.text.strip('\t\r\n'), url=url_obj['href'])
                scraped_results.append(search_result)

            return scraped_results

        else:
            return []

    def _parse_authors(self, raw_string: str) -> List[str]:
        stripped_string = raw_string.replace('by', '').strip()
        split_authors = [a.strip() for a in stripped_string.split(',')]

        return split_authors

    async def parse_detailed_view_of_search_result_async(self, search_result: BookEntry) -> BookSelectionDetails:

        if search_result.url is None:
            raise ValueError('Passed search result has a missing URL')

        endpoint = self.base_url + search_result.url
        page_content = await self._bsoup_from_url_async(endpoint)

        description: str = page_content.find(id='description').select_one('span[style~="display:none"]').text.strip('\r\n\t ')
        # TODO - add safety checks
        cover: str = page_content.find(id='coverImage')['src']
        title: str = page_content.find(id='bookTitle').text.strip('\r\n\t ')
        series: str = page_content.find(id='bookSeries').text.strip('\r\n\t ')
        genre_list_obj: ResultSet[BSoup] = page_content.find_all('a', class_='bookPageGenreLink')
        genres: List[str] = [genre_obj.text for genre_obj in genre_list_obj]

        raw_authors: str = page_content.find(id='bookAuthors').text.replace('\n', ' ')

        related_books_obj: ResultSet[BSoup] = page_content.select('[id^=bookCover]>a[href]')

        related_books: List[BookEntry] = []

        for book_obj in related_books_obj:

            title: str = book_obj.select_one('img')['alt']

            book_entry = BookEntry(
                title=title,
                url=book_obj['href']
            )

            related_books.append(book_entry)

        rating = page_content.find('span', {'itemprop': 'ratingValue'}).text.strip('\n\r\t ')

        pages = page_content.find('span', {'itemprop': 'numberOfPages'}).text.strip('\n\t\r ')

        return BookSelectionDetails(
            authors=self._parse_authors(raw_authors),
            description=description,
            cover_image_url=cover,
            genres=genres,
            title=title,
            series=series,
            related_books=related_books,
            rating=rating,
            pages=pages
        )

from typing import List, Sequence

from bs4 import BeautifulSoup as BSoup, ResultSet, Tag

from helpers.http_util import HttpUtil
from helpers.string_helper import StringHelper
from models.BookSelection import BookSelectionDetails, BookSelection


class BookPageLocators:
    DESCRIPTION = '#description>span[style~="display:none"]'
    COVER = '#coverImage'
    TITLE = '#bookTitle'
    SERIES = '#bookSeries'
    GENRES = 'a.bookPageGenreLink'
    AUTHORS = '#bookAuthors'
    RATING = 'span[itemprop="ratingValue"]'
    PAGES = 'span[itemprop="numberOfPages"]'
    RELATED_BOOKS = '[id^=bookCover]>a[href]'


class BookPage:

    def __init__(self, base_url):
        self.base_url = base_url

    def _parse_authors(self, raw_string: str) -> List[str]:
        stripped_string = raw_string.replace('by', '').strip()
        split_authors = [a.strip() for a in stripped_string.split(',')]

        return split_authors

    def _get_related_books(self, related_books_obj: Sequence[BSoup]) -> List[BookSelection]:

        related_books: List[BookSelection] = []

        for book_obj in related_books_obj:
            title: str = book_obj.select_one('img')['alt']

            book_entry = BookSelection(
                title=title,
                url=book_obj['href']
            )

            related_books.append(book_entry)

        return related_books

    async def parse_detailed_book_view_async(self, search_result: BookSelection) -> BookSelectionDetails:

        if search_result.url is None:
            raise ValueError('Passed search result has a missing URL')

        endpoint = self.base_url + search_result.url
        page_content = await HttpUtil.bsoup_from_url_async(endpoint)

        description = StringHelper.to_stripped_text(page_content.select_one(BookPageLocators.DESCRIPTION))
        cover: str = page_content.select_one(BookPageLocators.COVER)['src']
        title: str = StringHelper.to_stripped_text(page_content.select_one(BookPageLocators.TITLE))
        series: str = StringHelper.to_stripped_text(page_content.select_one(BookPageLocators.SERIES))
        raw_authors: str = StringHelper.to_stripped_text(page_content.select_one(BookPageLocators.AUTHORS))
        rating = StringHelper.to_stripped_text(page_content.select_one(BookPageLocators.RATING))
        pages = StringHelper.to_stripped_text(page_content.select_one(BookPageLocators.PAGES))
        related_books_obj: ResultSet[BSoup] = page_content.select(BookPageLocators.RELATED_BOOKS)
        genre_list_obj: ResultSet[BSoup] = page_content.select(BookPageLocators.GENRES)
        genres: List[str] = [genre_obj.text for genre_obj in genre_list_obj]

        return BookSelectionDetails(
            authors=self._parse_authors(raw_authors),
            description=description,
            cover_image_url=cover,
            genres=genres,
            title=title,
            series=series,
            related_books=self._get_related_books(related_books_obj),
            rating=rating,
            pages=pages
        )
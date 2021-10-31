from typing import Optional, List

from pydantic import BaseModel


class BookSelection(BaseModel):
    url: Optional[str]
    title: Optional[str]


class BookSelectionDetails(BaseModel):
    description: str
    cover_image_url: str
    title: str
    series: Optional[str]
    authors: List[str]
    genres: List[str]
    related_books: List[BookSelection]
    rating: str
    pages: str

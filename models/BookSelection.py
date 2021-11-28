from typing import Optional, List

from pydantic import BaseModel

from helpers.model_utils import to_camel_case


class BookSelection(BaseModel):
    url: Optional[str]
    title: Optional[str]


class BookSelectionList(BaseModel):
    __root__: List[BookSelection]


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

    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True

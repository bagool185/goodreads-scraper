from ctypes import Union

from bs4 import Tag, BeautifulSoup as BSoup


class StringHelper:

    @staticmethod
    def to_stripped_text(obj: BSoup) -> str:
        if obj is None:
            raise ValueError('Missing required property when trying to strip text')

        return obj.text.strip('\r\n\t ')

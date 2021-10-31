import aiohttp
from bs4 import BeautifulSoup as BSoup


class HttpUtil:
    @staticmethod
    async def bsoup_from_url_async(url: str) -> BSoup:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return BSoup(await response.text(), 'html.parser')

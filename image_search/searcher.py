import asyncio
import random
from io import BytesIO

import aiohttp
import async_cse

TYPE_TO_FORMAT = {
    "image/png": "png",
    "image/svg+xml": "svg",
    "image/jpeg": "jpeg",
    "image/webp": "webp",
    "image/gif": "gif"
}


class Searcher:
    def __init__(self, tokens: list[str]):
        self.client = async_cse.Search(tokens)

    async def search_image(self, query: str, safe_search=False) -> list[async_cse.Result]:
        return await self.client.search(query, safesearch=safe_search, image_search=True)

    @staticmethod
    async def _get_file_extension(content_type: str) -> str:
        if content_type not in TYPE_TO_FORMAT:
            print(content_type)
        return TYPE_TO_FORMAT.get(content_type, "png")

    @staticmethod
    async def get_image(url: str) -> tuple[str, BytesIO] | None:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector()) as session:
            async with session.get(url.replace("https", "http"), timeout=2) as response:
                if response.status != 200:
                    return None
                return (await Searcher._get_file_extension(response.content_type)), BytesIO(
                    await response.content.read())

    async def search_get_image(self, query: str, shuffle: bool = True, **kwargs) -> tuple[str,
                                                                                          BytesIO]:
        images = await self.search_image(query, **kwargs)
        if shuffle:
            random.shuffle(images)
        images_iter = iter(images)
        image_object = None
        while not image_object:
            try:
                image_object = await self.get_image(next(images_iter).image_url)
            except (aiohttp.client.ClientError, asyncio.exceptions.TimeoutError):
                continue
            except StopIteration:
                raise ValueError("Не удалось скачать ни одну картинку.")
        return image_object

    def __del__(self):
        self.client.close()

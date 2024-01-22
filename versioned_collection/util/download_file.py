import aiohttp


async def download_file(url: str) -> str:
    """
    Download a file from a url.

    :param url: The url
    :return: The file contents
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

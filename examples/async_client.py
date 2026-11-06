"""Use the asyncio client."""

import asyncio

from asin import AsyncAsinClient


async def main() -> None:
    async with AsyncAsinClient() as client:  # reads ASIN_API_KEY
        response = await client.search_amazon(query="wireless earbuds")
        print(response.data)


asyncio.run(main())

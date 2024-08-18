import asyncio
from aiohttp import ClientSession, ClientTimeout

from src.util import async_timed, fetch_status


@async_timed()
async def main():
    session_timeout = ClientTimeout(total=1, connect=0.1)
    request_timeout = ClientTimeout(total=0.2)
    async with ClientSession(timeout=session_timeout) as session:
        url = "https://www.example.com"
        try:
            status = await fetch_status(session, url, request_timeout)
            print(f"Status for url: {url} was {status}")
        except TimeoutError:
            print("Request timed out!")


asyncio.run(main())
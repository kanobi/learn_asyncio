import asyncio
from aiohttp import ClientSession, ClientTimeout

from src.util import async_timed, fetch_status

TOTAL_REQS = 3000

@async_timed()
async def main():
    session_timeout = ClientTimeout(total=60, connect=0.1)
    request_timeout = ClientTimeout(total=10)
    async with ClientSession(timeout=session_timeout) as session:
        urls = ["https://www.example.com" for _ in range(TOTAL_REQS)]
        requests = [fetch_status(session, url, request_timeout) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


asyncio.run(main())
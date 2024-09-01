import asyncio
from aiohttp import ClientSession, ClientTimeout
from src.util import async_timed


@async_timed()
async def fetch_status(
    session: ClientSession,
    url: str,
    timeout: ClientTimeout = None,
    delay: int=0,
) -> int:
    if delay:
        await asyncio.sleep(delay)
    async with session.get(url, timeout=timeout) as result:
        return result.status
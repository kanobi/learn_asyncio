import asyncio
from src import util


async def main() -> None:
    sleep_1 = asyncio.create_task(util.delay(3))
    sleep_2 = asyncio.create_task(util.delay(3))
    sleep_3 = asyncio.create_task(util.delay(3))

    await sleep_1
    await sleep_2
    await sleep_3

asyncio.run(main())

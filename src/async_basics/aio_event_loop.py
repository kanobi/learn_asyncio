import asyncio
from src.util import delay


def call_later():
    print("I'm being called in the future")


async def main() -> None:
    event_loop = asyncio.get_running_loop()
    event_loop.call_soon(call_later)
    await delay(1)

asyncio.run(main())

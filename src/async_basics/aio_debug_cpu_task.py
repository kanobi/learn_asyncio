import asyncio
from src.util import async_timed


@async_timed()
async def cpu_bound() -> int:
    count = 0
    for i in range(10_000_000):
        count += 1
    return count


def call_later():
    print("I'm being called in the future")


async def main() -> None:
    event_loop = asyncio.get_event_loop()
    event_loop.slow_callback_duration = .1
    task = asyncio.create_task(cpu_bound())
    await task

asyncio.run(main(), debug=True)

import asyncio

from src.util import delay


async def hello_every_second(seconds: int):
    for i in range(seconds):
        await asyncio.sleep(1)
        print("I'm running other code while waiting...")


async def main() -> None:
    sleep_1 = asyncio.create_task(delay(3))
    sleep_2 = asyncio.create_task(delay(3))

    await hello_every_second(2)
    await sleep_1
    await sleep_2

asyncio.run(main())

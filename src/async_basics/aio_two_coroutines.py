import asyncio

from src.util import delay


async def add_one(number: int) -> int:
    return number + 1


async def hello_world_msg() -> str:
    await delay(1)
    return "Hello world"


async def main() -> None:
    msg = await hello_world_msg()
    result = await add_one(1)
    print(result)
    print(msg)


asyncio.run(main())

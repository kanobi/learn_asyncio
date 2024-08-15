import asyncio
from asyncio import Future


async def set_future_value(future: Future) -> None:
    await asyncio.sleep(1)
    future.set_result(42)


def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))
    return future


async def main() -> None:
    future = make_request()
    print(f"Is the future done: {future.done()}")
    value = await future
    print(f"Is the future done: {future.done()}")
    print(value)

asyncio.run(main())

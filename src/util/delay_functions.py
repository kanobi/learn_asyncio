import asyncio


async def delay(seconds: int) -> int:
    print(f"Sleeping for {seconds} second(s)")
    await asyncio.sleep(seconds)
    print(f"Finished sleeping for {seconds} second(s)")
    return seconds

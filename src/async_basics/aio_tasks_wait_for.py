import asyncio
from asyncio.exceptions import TimeoutError

from src.util import delay


async def main() -> None:
    sleep_1 = asyncio.create_task(delay(3))

    try:
        result = await asyncio.wait_for(sleep_1, timeout=1)
        print(result)
    except TimeoutError:
        cancelled = "Yes" if sleep_1.cancelled() else "No"
        print(
            f"Got a timeout. Was a task cancelled: {cancelled}"
        )

asyncio.run(main())

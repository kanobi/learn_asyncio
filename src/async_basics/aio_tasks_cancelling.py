import asyncio
from asyncio import CancelledError

from src.util import delay, async_timed


@async_timed()
async def main() -> None:
    long_task = asyncio.create_task(delay(10))
    elapsed_seconds = 0
    while not long_task.done():
        print("Task not finished. Checking again in a sec...")
        await asyncio.sleep(1)
        elapsed_seconds += 1
        if elapsed_seconds >= 5:
            print("Task is taking too long. Cancelling...")
            long_task.cancel()

    try:
        await long_task
    except CancelledError as e:
        print("Our task was cancelled")
        print(e)

asyncio.run(main())

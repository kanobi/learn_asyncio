import asyncio
from aiohttp import ClientSession

from src.util import async_timed, fetch_status


@async_timed()
async def failed_on_exception():
    async with ClientSession() as session:
        urls = ["https://www.example.com", "invalid://example.com"]
        tasks = [fetch_status(session, url) for url in urls]    
        status_codes = await asyncio.gather(*tasks)
        print(status_codes)


@async_timed()
async def return_exceptions():
    async with ClientSession() as session:
        urls = ["https://www.example.com", "invalid://example.com"]
        tasks = [fetch_status(session, url) for url in urls]    
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        exceptions = [res for res in results if isinstance(res, Exception)]
        successes = [res for res in results if not isinstance(res, Exception)]
        
        print(f"Exceptions: {exceptions}")
        print(f"Successes: {successes}")


@async_timed()
async def process_as_completed():
    async with ClientSession() as session:
        URL = "https://www.example.com"
        tasks = [
            fetch_status(session, URL, delay=1),
            fetch_status(session, URL, delay=1),
            fetch_status(session, URL, delay=10),
        ]
        for finished_task in asyncio.as_completed(tasks):
            print(await finished_task)
            

@async_timed()
async def process_as_completed_timeouts():
    URL = "https://www.example.com"
    TASK_TIMEOUT = 6
    async with ClientSession() as session:
        tasks = [
            fetch_status(session, URL, delay=1),
            fetch_status(session, URL, delay=5),
            fetch_status(session, URL, delay=10),
        ]
        for finished_task in asyncio.as_completed(tasks, timeout=TASK_TIMEOUT):
            try:
                print(await finished_task)
            except asyncio.TimeoutError:
                print(f"We got a timeout for task: {finished_task}")
        
        print("Status of tasks in the loop: ")
        for task in asyncio.tasks.all_tasks():
            print(task)


#print("first run:")
#asyncio.run(failed_on_exception())

print("--------------")
print("now for handling exceptions:")

asyncio.run(return_exceptions())

# using as_completed to process requests as they are completed
print("--------------")
print("now for processing as_completed:")

asyncio.run(process_as_completed())


# using process_as_completed_timeouts where we introduce timeouts 
print("--------------")
print("now for process_as_completed_timeouts:")

asyncio.run(process_as_completed_timeouts())
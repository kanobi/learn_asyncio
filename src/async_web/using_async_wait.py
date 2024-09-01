import asyncio
from asyncio import create_task
import logging

from aiohttp import ClientSession

from src.util import async_timed, fetch_status

URL = "https://www.example.com"
BADURL = "python://www.example.com"


@async_timed()
async def process_async_wait():
    async with ClientSession() as session:
        tasks = [
            create_task(fetch_status(session, URL, delay=1)),
            create_task(fetch_status(session, URL, delay=1)),
        ]
        
        # pending will always be empty,
        # since wait() uses (return_when: ALL_COMPLETED) by default.
        done, pending = await asyncio.wait(tasks)
        
        print(f"Done tasks: {done}")
        print(f"Pending tasks: {pending}")
        
        for done_task in done:
            print(await done_task)


@async_timed()
async def process_exceptions_with_wait():
    async with ClientSession() as session:
        tasks = [
            create_task(fetch_status(session, URL)),
            create_task(fetch_status(session, BADURL)),
        ]
        
        # pending will always be empty,
        # since wait() uses (return_when: ALL_COMPLETED) by default.
        done, pending = await asyncio.wait(tasks)
        
        print(f"Done tasks: {done}")
        print(f"Pending tasks: {pending}")
        
        for done_task in done:
            if done_task.exception() is None:
                logging.info(done_task.result())
            else:
                logging.error("Request got exception", exc_info=done_task.exception())


@async_timed()
async def cancel_pending_tasks():
    async with ClientSession() as session:
        tasks = [
            create_task(fetch_status(session, BADURL)),
            create_task(fetch_status(session, URL, delay=5)),
            create_task(fetch_status(session, URL, delay=5)),
        ]
        
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
        
        print(f"Done tasks: {done}")
        print(f"Pending tasks: {pending}")
        
        for done_task in done:
            if done_task.exception() is None:
                logging.info(done_task.result())
            else:
                logging.error("Request got exception", exc_info=done_task.exception())
        
        for pending_task in pending:
            pending_task.cancel()


@async_timed()
async def process_as_they_complete():
    async with ClientSession() as session:
        pending = [
            create_task(fetch_status(session, URL, delay=5)),
            create_task(fetch_status(session, URL, delay=1)),
            create_task(fetch_status(session, URL)),
        ]
        
        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED
            )
        
            print(f"Done tasks: {len(done)}")
            print(f"Pending tasks: {len(pending)}")
        
            for done_task in done:
                if done_task.exception() is None:
                    logging.info(done_task.result())
                else:
                    logging.error(
                        "Request got exception",
                        # exc_info=done_task.exception(),
                    )
                    for pending_task in pending:
                        pending_task.cancel()
                    pending = None
                

# print("--------------")
# print("now for process_async_wait:")
# asyncio.run(process_async_wait())

# print("--------------")
# print("now for process_exceptions_with_wait:")
# asyncio.run(process_exceptions_with_wait())

# print("--------------")
# print("now for cancel_pending_tasks:")
# asyncio.run(cancel_pending_tasks())

print("--------------")
print("now for process_as_they_complete:")
asyncio.run(process_as_they_complete())
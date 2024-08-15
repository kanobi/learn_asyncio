import time
from functools import wraps
from typing import Any, Callable


def async_timed():

    def wrapper(func: Callable) -> Callable:

        @wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f"Starting {func} ({args}, {kwargs})")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                print(f"Finished {func} in {end-start:.4f} second(s)")

        return wrapped

    return wrapper

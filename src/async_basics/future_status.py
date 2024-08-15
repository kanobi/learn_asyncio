from asyncio import Future

my_future = Future()
print(f"Future status: {my_future.done()}")
my_future.set_result(42)
print(f"Future status: {my_future.done()}")
print(f"Future result: {my_future.result()}")

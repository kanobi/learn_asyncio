import os
import threading
import time


def hello_from_thread():
    print(f">> Hi from thread: {threading.current_thread().name}")
    time.sleep(1)
    print(">> Exiting thread")


print(f"Running process id: {os.getpid()}")
print(f"Currently running {threading.active_count()} threads")
print(f"Main thread: {threading.current_thread().name}")

hello_thread = threading.Thread(target=hello_from_thread)
hello_thread.start()

total_threads = threading.active_count()
thread_name = threading.current_thread().name

print(f"Currently running {total_threads} threads")
print(f"Main thread: {thread_name}")
print("Waiting for all threads to finish")

hello_thread.join()

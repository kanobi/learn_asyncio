import multiprocessing
import os
import time


def hello_from_proc():
    pid = os.getpid()
    print(f"{pid} >> child started")
    print(f"{pid} >> waiting for a sec...")
    time.sleep(2)
    print(f"{pid} >> exiting")


if __name__ == "__main__":
    pid = os.getpid()
    print(f"Parent proces: {pid}")
    c_proc = multiprocessing.Process(target=hello_from_proc)
    c_proc.start()
    print("Parent: doing some work.")
    time.sleep(1)
    print("Parent finished")
    c_proc.join()
    print("All finished")

import time
import threading


def print_fib(number):
    def fib(n):
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return fib(n - 1) + fib(n - 2)

    print(f"Fib({number}) = {fib(number)}")


def fib_no_threading():
    print_fib(40)
    print_fib(41)


def fib_threading():
    f1 = threading.Thread(target=print_fib, args=(40, ))
    f2 = threading.Thread(target=print_fib, args=(41, ))

    f1.start()
    f2.start()

    f1.join()
    f2.join()


print("Starting...")
start = time.time()
fib_no_threading()
end = time.time()

print(f"Completed in {end - start:.4f} seconds")

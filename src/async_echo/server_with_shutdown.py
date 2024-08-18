import asyncio
import logging
import signal
import socket
from asyncio import AbstractEventLoop
from typing import List


PORT = 8000
ADDR = "127.0.0.1"
RECEIVE_BYTES_LEN = 32
SHUTDOWN_SEC = 3


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # loop forever, waiting for data from client connection
    con_addr, con_port = connection.getpeername()
    try:
        while data := await loop.sock_recv(connection, RECEIVE_BYTES_LEN):
            # once we have data, send it back to client
            print(f"Received data {data}[{len(data)}], from conn: {con_addr}:{con_port}")
            if data == b"boom\r\n":
                raise RuntimeError("Boom received!")
            await loop.sock_sendall(connection, data)
    except Exception as e:
        logging.exception(e)
    finally:
        connection.close()


echo_tasks = []


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop) -> None:
    while True:
        print(f"Listening for new connections...")
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got connection from {address}")
        echo_tasks.append(asyncio.create_task(echo(connection, loop)))


async def close_tasks(tasks: List[asyncio.Task]) -> None:    
    waiters = [asyncio.wait_for(task, SHUTDOWN_SEC) for task in tasks]
    if waiters:
        print("Gracefully shutting down!")
    else:
        print("Shutting down!")
        return

    for waiter_task in waiters:
        try:
            await waiter_task
        except asyncio.exceptions.TimeoutError:
            pass


async def main():
    server_address = (ADDR, PORT)
    server_socket = socket.socket(
        socket.AF_INET,      #  type of address - address:port
        socket.SOCK_STREAM,  #  protocol - TCP
    )
    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR, #  reuse port after restarting app
        1,
    )
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {"SIGINT", "SIGTERM"}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    await listen_for_connection(server_socket, loop)


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_tasks(echo_tasks))
finally:
    loop.close()

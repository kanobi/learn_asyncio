import asyncio
import socket
from asyncio import AbstractEventLoop


PORT = 8000
ADDR = "127.0.0.1"
RECEIVE_BYTES_LEN = 32


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    # loop forever, waiting for data from client connection
    con_addr, con_port = connection.getpeername()
    while data := await loop.sock_recv(connection, RECEIVE_BYTES_LEN):
        # once we have data, send it back to client
        print(f"Received data {data}[{len(data)}], from conn: {con_addr}:{con_port}")
        await loop.sock_sendall(connection, data)


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop) -> None:
    while True:
        print(f"Listening for new connections...")
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got connection from {address}")
        asyncio.create_task(echo(connection, loop))


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

    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())
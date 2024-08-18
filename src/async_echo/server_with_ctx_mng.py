import asyncio
import socket


PORT = 8000
ADDR = "127.0.0.1"
RECEIVE_BYTES_LEN = 32


class ConnectedSocket:

    def __init__(self, server_socket) -> None:
        self._connection = None
        self._server_socket = server_socket
    
    async def __aenter__(self) -> socket:
        # This coroutine is called when we enter the 'with' block.
        # It waits until client connects and returns connection.
        print("Entered context manager. Waiting for the connection...")
        loop = asyncio.get_event_loop()
        connection, _ = await loop.sock_accept(self._server_socket)
        self._connection = connection
        con_addr, con_port = connection.getpeername()
        print(f"Accepted connection from: {con_addr}:{con_port}")
        return self._connection

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        # This coroutine is called when we exit 'with' block.
        # We clean up any resource we used. In this case just close the connection.
        print("Exiting context manager.")
        self._connection.close()
        print("Closed connection.")


async def main():
    loop = asyncio.get_event_loop()
    
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

    # this calls __aenter__
    async with ConnectedSocket(server_socket) as connection:
        data = await loop.sock_recv(connection, RECEIVE_BYTES_LEN)
        print(data)
        # after this __aexit__ will execute and we'll close the connection.


asyncio.run(main())
import selectors
import socket
from selectors import SelectorKey

PORT = 8000
ADDR = "127.0.0.1"
ESCAPE_CHAR = b"\r\n"

server_socket = socket.socket(
    socket.AF_INET,  # type of address - address:port
    socket.SOCK_STREAM,  # protocol - TCP
)
server_socket.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,  # reuse port after restarting app
    1,
)
selector = selectors.DefaultSelector()

address = (ADDR, PORT)
server_socket.bind(address)
server_socket.listen()
server_socket.setblocking(False)
print(f"Server listening on {ADDR}:{PORT}")

# register default selector
selector.register(server_socket, selectors.EVENT_READ)

while True:
    # creates selector that will timeout after 1 sec
    events: list[tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0:
        print("No events, waiting a bit more.")

    for event, _ in events:
        # socket for the event is stored in fileobj field
        event_socket = event.fileobj
        if event_socket == server_socket:
            # if event socket is the same as server socket,
            # we know that this is connection attempt
            new_conn, client_address = server_socket.accept()
            new_conn.setblocking(False)
            print(f"I got connection from {client_address}")
            # register client that connected with our selector
            selector.register(new_conn, selectors.EVENT_READ)
        else:
            # otherwise, receive the data and echo it back
            data = event_socket.recv(1024)
            print(f"I got data: {data}")
            event_socket.send(data)

import socket

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

address = (ADDR, PORT)
server_socket.bind(address)
server_socket.listen()
print(f"Server listening on {ADDR}:{PORT}")

try:
    connections = []
    while True:
        # this will block until we get a connection
        new_conn, client_address = server_socket.accept()
        print(f"I got connection from {client_address}")
        connections.append(new_conn)
        for connection in connections:
            buffer = b""
            while buffer[-2:] != ESCAPE_CHAR:
                data = connection.recv(2)
                if not data:
                    break
                print(f"I got data: {data}")
                buffer += data
            print(f"All data received: {buffer}")
            connection.send(b"Echo: " + buffer)
finally:
    server_socket.close()

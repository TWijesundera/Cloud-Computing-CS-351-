"""P2P Server Class

    This class acts as the torrent server. It gives connections
        the IP and port to connect to other clients directly

    Author: Thisara Wijesundera
    CS 351
    Assignment 4
"""

import sys
import socket
import select

class Server:

    def __init__(self, HOST: str, PORT: int):
        self._connected_users = {}

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((HOST, PORT))
        self._server_socket.listen(10)
        print(f"Chat server started on port {str(PORT)}\n")
        
        self._connected_users[self._server_socket.getsockname()] = self._server_socket

    def start_server(self):
        address_second_connect = ""
        port_second_connect = 9009
        server_socket = self._server_socket

        while True:
            ready_to_read, ready_to_write, in_error = select.select(self._connected_users.values(), [], [], 0)

            for read_sock in ready_to_read:
                if read_sock == server_socket:
                    new_conn, addr = server_socket.accept()
                    self._connected_users[addr] = new_conn
                    print(f"Client {addr} connected\n")
                    
                    if len(self._connected_users) > 2:
                        # Send the address the new user should connect to
                        new_conn.send(addr[0])
                    else:
                        msg = "serverPeer"
                        new_conn.send(bytes(msg, 'UTF-8'))
                else:
                    try:
                        data = read_sock.recv(4096).decode('UTF-8')
                        if data:
                            port_second_connect = data if data.isdigit() else 9000
                            print(f"The next peer will connect to {addr} on port {port_second_connect}")
                        else:
                            print(f"Client {addr} is offline\n")
                            # Person left the server
                            if read_sock.getpeername() in self._connected_users:
                                self._connected_users.pop(read_sock.getpeername())

                    except socket.error as msg:
                        print(msg)
                        # Tell the first user they should open a connection
if __name__ == "__main__":
    try:
        server = Server("0.0.0.0", 9009)
        server.start_server()

    except KeyboardInterrupt:
        server._server_socket.close()
        sys.exit()
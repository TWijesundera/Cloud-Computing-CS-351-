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
        """Creates the Server object

            Binds a socket instance to 0.0.0.0 on port 9009

            Instance Variables:
                _connected_user (Dict): Dictionary of users that have connected
                    to the server
                _server_socket (Socket Object): Servers socket object
        """
        self._connected_users = {}

        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((HOST, PORT))
        self._server_socket.listen(10)
        print(f"Chat server started on port {PORT}\n")
        
        self._connected_users[self._server_socket.getsockname()] = self._server_socket

    def start_server(self):
        """Starts the torrent server

            Users connect to the torrent server
            The torrent server tells the client who to connect to directly

            Variables:
                second_address (str): The address the second client should connect to
                second_port (int): The port the second client should connect to
                new_conn (Socket Object): 
        """
        second_address = ""
        second_port = 9009
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
                        new_conn.send(bytes(f"{second_address} {second_port}", 'UTF-8'))
                    else:
                        msg = "serverPeer"
                        new_conn.send(bytes(msg, 'UTF-8'))
                else:
                    try:
                        data = read_sock.recv(4096).decode('UTF-8')
                        if data:
                            second_port = data if data.isdigit() else 9009
                            second_address = addr[0]
                            print(f"The next peer will connect to {second_address} on port {second_port}")
                        else:
                            print(f"Client {addr} is offline\n")
                            # Person left the server
                            if read_sock.getpeername() in self._connected_users:
                                self._connected_users.pop(read_sock.getpeername())

                    except socket.error as msg:
                        print(msg)
                        # Tell the first user they should open a connection
if __name__ == "__main__":
    """Main method

        Create a server object and begin allowing
            users to connect
    """
    try:
        server = Server("0.0.0.0", 9009)
        server.start_server()

    except KeyboardInterrupt:
        server._server_socket.close()
        sys.exit()
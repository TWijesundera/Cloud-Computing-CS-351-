import sys
import socket
import select

from Board import Board
from typing import Dict, List

count = 0
RECV_BUFFER = 4096

class Server:
    
    symbol = 'X'

    def __init__(self, HOST, PORT):
        """Initilize server with some variables

            Variables:
                player_sockets (Dict): key - address       values - tuple(socket object, 'x' or 'o')
                board (Board): Initalize the Tic Tac Toe board object
        """
        self.game_board = Board()
        self.players_sockets = {}
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(10)
            print(f"Chat server started on port {str(PORT)}\n")

            # add server socket object to the list of readable connections
            self.players_sockets[self.server_socket.getsockname()] = (self.server_socket, 'server')
        except socket.error as msg:
            print(f"ERROR {msg}")
            sys.exit()

    def broadcast_board(self):
        pass

    def chat_server(self):
        while True:
            server_socket = self.server_socket
            try:
                # get the list sockets which are ready to be read through select
                # 4th arg, time_out  = 0 : poll and never block
                ready_to_read,ready_to_write,in_error = select.select([x[0] for x in self.players_sockets.values()],[],[],0)
            
                for sock in ready_to_read:
                    # print("ready list: {} ".format(ready_to_read))
                    # print("ready sock {} ".format(sock))
                    # a new connection request recieved
                    if sock == server_socket: 
                        sockfd, addr = server_socket.accept()
                        self.players_sockets[addr] = (sockfd, self.assign_player())
                        # print(f"\nsocket list: {self.players_sockets}\n")
                        print ("Client (%s, %s) connected" % addr)
                        
                        self.broadcast(sockfd, "[%s:%s] entered the chat room\n" % addr)
                    
                    # a message from a client, not a new connection
                    else:
                        # process data recieved from client, 
                        try:
                            # receiving data from the socket.
                            data = sock.recv(RECV_BUFFER).decode('UTF-8')
                            # print(f"after data recv else statement: {data}")
                            if data:
                                # there is something in the socket
                                # print(f"recieved data: {data}")
                                self.broadcast(sock, f"\r[{str(sock.getpeername())}] {data}")  
                            else:
                                # remove the socket that's broken    
                                if sock in self.players_sockets:
                                    # print("Sock in else: {}".format(sock))
                                    self.players_sockets.pop(sock.getpeername())

                                # at this stage, no data means probably the connection has been broken
                                self.broadcast(sock, "Client (%s, %s) is offline\n" % addr) 

                        # exception 
                        except Exception as e:
                            # print(f"execption offline : {e}\n")
                            self.broadcast(sock, "Client (%s, %s) is offline\n" % addr)
                            continue
            except KeyboardInterrupt:
                return
    
    # broadcast chat messages to all connected clients
    def broadcast (self, sock, message):
    #whoTo = 0 send only x player
    #whoTO = 1 send to only Y
    #whoTo = 2 send to all
        print(f"sockfd: {sock}\n")
        for socket in self.players_sockets:
            # send the message only to peer
            print(f"if {socket} != {self.server_socket.getsockname()} and {socket} != {sock.getpeername()}")
            if socket != self.server_socket.getsockname() and socket != sock.getpeername():
                try :
                    # print(f"\"{message}\" sent to: {socket}")
                    self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                except Exception as e:
                    # broken socket connection
                    self.players_sockets[socket][0].close()
                    # broken socket, remove it
                    if socket in self.players_sockets:
                        self.players_sockets.pop(socket)
                    print("\nERROR: {e}\n")

    def assign_player(self):
        """ Assigns the player to X or O
        """
        symbol = Server.symbol

        if Server.symbol == 'X':
            Server.symbol = 'O'
        else:
            Server.symbol = 'X'
        
        return symbol
 
if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 9009
    server = Server(HOST, PORT)
    try:
        print(server.game_board.__str__())
        server.chat_server()
    
    except KeyboardInterrupt:
        server.server_socket.close()
        sys.exit()

"""
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit()
        """

import sys
import socket
import select

from Board import Board
from typing import Dict, List

count = 0
RECV_BUFFER = 4096

class Server:
    """Server for tic tac toe game

        Variables:
            Server.symbol (str): Keeps track of what team to assign client
    """
    
    symbol = 'X'
    game_started = (False, False) # Represents (There is an x player ready, there is an O player ready)

    def __init__(self, HOST, PORT):
        """Initilize server with some variables

            Variables:
                player_sockets (Dict): key - address       values - tuple(socket object, 'x' or 'o')
                board (Board): Initalize the Tic Tac Toe board object
                server_socket (Socket): Keeps track of the servers socket object
        """
        self.game_board = Board()
        self.players_sockets = {}
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((HOST, PORT))
            self.server_socket.listen(10)
            print(f"Chat server started on port {str(PORT)}\n")

            # add server socket object to the dict of readable connections
            self.players_sockets[self.server_socket.getsockname()] = (self.server_socket, 'server')
        except socket.error as msg:
            print(f"ERROR {msg}")
            sys.exit()

    def broadcast_board(self):
        pass

    def check_if_ready(self, message):
        """Check if all the players are ready to begin the game
        """
        for socket in self.players_sockets:
            # send the message to all peers
            if socket != self.server_socket.getsockname():
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


    def chat_server(self):
        """Starts the server loop

            Recieves data communication from all clients connect to the server

            Algorithm:
                Check if there are 3 player sockets and one is X and one is O 
                X goes first
                Recieve data and check if it's from an x player.
                If data comes in as (x,x) then the server should parse the position
                    Send position to Board object
                Else
                    Text data gets sent to everyone
        """
        while True:
            server_socket = self.server_socket
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
                    
                    if len(self.players_sockets) >= 3:
                        self.check_if_ready("Are you ready to play tic tac toe?\n") # Change to broadcast
                    # self.broadcast(sockfd, "[%s:%s] entered the chat room\n" % addr)m
                
                # a message from a client, not a new connection
                else:
                    # process data recieved from client, 
                    try:
                        # receiving data from the socket.
                        data = sock.recv(RECV_BUFFER).decode('UTF-8')
                        # print(f"after data recv else statement: {data}")
                        if data:
                            if not all(Server.game_started):
                                if data.lower() == 'ready':
                                    if self.players_sockets[sock.getpeername()][1] == 'X' and not Server.game_started[0]:
                                        Server.game_started[0] = True
                                    elif self.players_sockets[sock.getpeername()][1] == 'O' and not Server.game_started[1]:
                                        Server.game_started[1] = True
                                # there is something in the socket
                                # print(f"recieved data: {data}")
                            else:
                                self.broadcast(sock, f"\r[{str(sock.getpeername())}] {data}")
                        else:
                            # remove the socket that's broken    
                            if sock in self.players_sockets:
                                # print("Sock in else: {}".format(sock))
                                self.players_sockets.pop(sock.getpeername())

                            # at this stage, no data means probably the connection has been broken
                            self.broadcast("Client {addr} is offline\n", sock) 

                    # exception 
                    except Exception as e:
                        print(f"ERROR peer offline: {e}\n")
                        self.broadcast(f"Client {addr} is offline\n", sock=sock)
                        continue
    
    # broadcast chat messages to all connected clients sock=NOne, whoTo=0
    def broadcast (self, message, **kwargs):
    #whoTo = 0 send to only X players (asking for move)
    #whoTO = 1 send to only O players (asking for move)
    #whoTo = 2 send to all players (position where person will play)
        # print(f"sockfd: {sock}\n")
        for socket in self.players_sockets:
            # send the message only to peer
            # print(f"if {socket} != {self.server_socket.getsockname()} and {socket} != {sock.getpeername()}")
            try:
                if whoTo not in kwargs:
                    # Try sending to all sockets
                    if socket != self.server_socket.getsockname():
                        self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                else:
                    if whoTo == 1:
                        # Broadcast to only X players
                        if socket != self.server_socket.getsockname() and socket != sock.getpeername():
                            if self.player_sockets[sock.getsockname()][1] == 'X':
                                self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                    else:
                        # Broadcast to only O players
                        if socket != self.server_socket.getsockname() and socket != sock.getpeername():
                            if self.player_sockets[sock.getsockname()][1] == 'O':
                                self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                        
            """
            except KeyError as e:
                print(f"\Key does not exist: {e}\n")
            
            except socket.error as e:
                            # broken socket connection
                            self.players_sockets[socket][0].close()
                            # broken socket, remove it
                            if socket in self.players_sockets:
                                self.players_sockets.pop(socket)
                            print("\nERROR: {e}\n")

            if socket != self.server_socket.getsockname() and socket != sock.getpeername():
                try :
                    # print(f"\"{message}\" sent to: {socket}")
                    self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                except Exception as e:
                    # broken socket connection
                    self.players_sockets[socket][0].close()
                    # broken sockeExceptiont, remove it
                    if socket in self.players_sockets:
                        self.players_sockets.pop(socket)
                    print("\nERROR: {e}\n")
            """

    def assign_player(self) -> str:
        """ Assigns the player to X or O

            Modifies the class variable Server.symbol
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

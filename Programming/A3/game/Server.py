import sys
import socket
import select
import re

from Board import Board
from typing import Dict, List
from collections import Counter

count = 0
RECV_BUFFER = 4096

class Server:
    """Server for tic tac toe game

        Variables:
            Server.symbol (str): Keeps track of what team to assign client
    """
    
    symbol = 'X'

    def __init__(self, HOST: str, PORT: int):
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

    def check_for_players(self):
        """ Checks if there are enough 'X' and 'O' players to play the game"""
        count = Counter(x[1] for x in self.players_sockets.values())
        return count.get('X', 0) >= 1 and count.get('O', 0) >= 1

    """def check_if_ready(self, message: str):
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
                    print(f"\nERROR: {e}\n")"""

    def sanitize_input(self, user_data: str, symbol: str) -> bool:
        """Checks and makes sure the input is correct and can be sent to update the board

            Args:
                user_data (str): Message the user sent

            Returns:
                True: Successfully able to update the board
                False: Unable to update board
        """
        user_in = re.findall(r"[^\W_]+", user_data)
        try:
            self.game_board.update_board(int(user_in[0]), int(user_in[1]), symbol)
            return True
        except IndexError:
            return False
        

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
        server_socket = self.server_socket
        game_started = False
        game_board = self.game_board
        turn = 'X'

        while True:
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read,ready_to_write,in_error = select.select([x[0] for x in self.players_sockets.values()],[],[],0)

            for read_sock in ready_to_read:
                # print("ready list: {} ".format(ready_to_read))
                # print("ready sock {} ".format(sock))
                # a new connection request recieved
                if read_sock == server_socket: 
                    print(f"Read sock: {read_sock}")
                    new_conn, addr = server_socket.accept()
                    self.players_sockets[addr] = (new_conn, self.assign_player())
                    # print(f"\nsocket list: {self.players_sockets}\n")
                    print (f"Client {addr} connected\n")

                    self.broadcast(f"{addr} entered the chat room\n", sock=new_conn)

                    if self.check_for_players():
                        print("tic tac toe")
                        self.broadcast(f"[server]: Let's begin tic tac toe\n")
                        print("broadcast board")
                        self.broadcast(f"[server]:\n{self.game_board.__str__()}\n")
                        game_started = True
                        if game_started:
                            print(f"turn: {turn}")
                            self.broadcast("[server]: It's your turn\n", whoTo=turn)
                    
                    elif not self.check_for_players() and len(self.players_sockets) == 1:   
                        print("not enough players")                           
                        self.broadcast("There are not enough players to continue. Ending game\n")
                        game_started = False

                # a message from a client, not a new connection
                else:
                    # process data recieved from client, 
                    try:
                        # receiving data from the socket.
                        data = read_sock.recv(RECV_BUFFER).decode('UTF-8')
                        # print(f"after data recv else statement: {data}")
                        if data:
                            if game_started:
                                """Check if the player input is valid
                                    Check if the person replying is the person who has a turn
                                        if not then just print their data
                                        else sanitize the input and switch the turn
                                """                                
                                if data[0] == '(':
                                    if self.players_sockets.get(read_sock.getpeername(), None)[1] == turn:
                                        """Check if the data from the person whose turn it is a move"""
                                        if self.sanitize_input(data, turn):
                                            print(game_board.__str__())
                                        else:
                                            self.broadcast(f"\r[{str(read_sock.getpeername())}]: {data}", sock=read_sock)
                                        # Switch turns
                                        turn = 'O' if turn == 'X' else 'X'
                                    else:
                                        self.broadcast(f"\r[{str(read_sock.getpeername())}]: {data}", sock=read_sock)
                                else:
                                    self.broadcast(f"\r[{str(read_sock.getpeername())}]: {data}", sock=read_sock)

                        else:
                            print(data)
                            # remove the socket that's broken    
                            if read_sock in self.players_sockets:
                                # print("Sock in else: {}".format(sock))
                                print(f"peer name: {read_sock.getpeername()}")
                                self.players_sockets.pop(read_sock)

                            # at this stage, no data means probably the connection has been broken
                            self.broadcast(f"Client {addr} is offline\n") 

                    # exception 
                    except Exception as e:
                        print(e)
                        self.broadcast(f"Client {addr} is offline\n")
                        continue
    
    # broadcast chat messages to all connected clients
    def broadcast (self, message: str, **kwargs: Dict):
    #whoTo = 0 send to only X players (asking for move)
    #whoTO = 1 send to only O players (asking for move)
    #whoTo = 2 send to all players (position where person will play)
        # print(f"sockfd: {sock}\n")
        server_name = self.server_socket.getsockname()
        if 'sock' in kwargs:
            socket_sent_msg = kwargs['sock'].getpeername()
        else:
            socket_sent_msg = server_name

        for socket in self.players_sockets.keys():
            # print(f"player keys: {socket}")
            # send the message only to peer
            # print(f"if {socket} != {self.server_socket.getsockname()} and {socket} != {sock.getpeername()}")
            try:
                if 'whoTo' not in kwargs:
                    # Try sending to all sockets
                    if socket != server_name and socket != socket_sent_msg:
                        self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                else:
                    if kwargs['whoTo'] == 'X':
                        print("broadcast to X")
                        # Broadcast to only X players
                        if socket != server_name and socket != socket_sent_msg and self.players_sockets[socket][1] == 'X':
                                self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
                    else:
                        # Broadcast to only O players
                        print("broadcast to O")
                        if socket != server_name and socket != socket_sent_msg and self.players_sockets[socket][1] == 'O':
                                self.players_sockets[socket][0].send(bytes(message, 'UTF-8'))
            except Exception as e:
                print(e)
                self.players_sockets[socket][0].close()
                # broken socket, remove it
                if socket in self.players_sockets:
                    self.players_sockets.pop(socket)
                print(f"\nERROR: {e}\n")
                        
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
        # print(server.game_board.__str__())
        server.chat_server()
    
    except KeyboardInterrupt:
        server.server_socket.close()
        print("\n")
        sys.exit()

"""
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit()
        """

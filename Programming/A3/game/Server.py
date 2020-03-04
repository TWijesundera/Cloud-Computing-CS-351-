"""This class controls a Chat and Tic Tac Toe game server

    Usage:
        python3 Server.py
        Server socket is bound to 0.0.0.0 on port 9009

    Requirements:
        Python 3.6: There are uses of f strings in this code

    Author: Thisara Wijesundera
    CS 351
    Assignment 3
"""

import sys
import socket
import select
import re

from typing import Dict
from collections import Counter

from Board import Board

class Server:
    """Server for tic tac toe game

        Binds on 0.0.0.0 on port 9009

        Notes:
            Improvements could be made on number of times
                the board object is accessed.
            Should implement tracking the number of moves
                and only checking if the board is full after a large number of moves
    """

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

    def check_for_players(self) -> bool:
        """Checks if there are enough 'X' and 'O' players to play the game

            Returns:
                True: If the count of X player and O players is greater
                    than or equal to 1
                False: If the count of X players or O players is less than 1
        """
        count = Counter(x[1] for x in self.players_sockets.values())
        return count.get('X', 0) >= 1 and count.get('O', 0) >= 1

    def sanitize_input(self, user_data: str, symbol: str) -> bool:
        """Checks and makes sure the input is correct and can be sent to update the board

            Args:
                user_data (str): Message the user sent
                symbol (str): The current symbol making the move

            Returns:
                True: Successfully able to update the board
                False: Unable to update board

            Notes:
                There could be some un-caught edge cases here
        """
        user_in = re.findall(r"[^\W_]+", user_data)
        try:
            self.game_board.update_board(int(user_in[0]), int(user_in[1]), symbol)
            return True
        except IndexError as msg:
            self.broadcast(f"ERROR: {msg}")
            return False

    def chat_server(self) -> None:
        """Starts the server loop

            Recieves data communication from all clients connect to the server
            Starts a tic tac toe game if there are enough players and allows
                them to chat with each other

            Algorithm:
                Check if there are 3 player sockets and one is X and one is O
                X goes first
                Recieve data and check if it's from an x player.
                If data comes in as (x,x) then the server should parse the position
                    Send position to Board object
                Else
                    Text data gets sent to everyone

            Improvements:
                Create a GUI for each user
                Create a way for players to whisper to their teammates
                Recognize commands so players can check which team their on again
        """
        server_socket = self.server_socket
        game_started = False
        game_board = self.game_board
        turn = 'X'
        assign_player = 'X'

        while True:
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read, ready_to_write, in_error = select.select([x[0] for x in self.players_sockets.values()], [], [], 0)

            for read_sock in ready_to_read:
                # print("ready list: {} ".format(ready_to_read))
                # print("ready sock {} ".format(sock))

                # a new connection request recieved
                if read_sock == server_socket:
                    new_conn, addr = server_socket.accept()
                    self.players_sockets[addr] = (new_conn, assign_player)
                    self.broadcast(f"You are an {assign_player} player\n", \
                                   sock=new_conn, whoTo="self")
                    assign_player = 'O' if assign_player == 'X' else 'X'
                    # print(f"\nsocket list: {self.players_sockets}\n")
                    print(f"Client {addr} connected\n")

                    self.broadcast(f"{addr} entered the chat room\n", sock=new_conn)

                    # Begin the game if there is 1 player for X and 1 for O
                    if self.check_for_players():
                        self.broadcast(f"[server]:Let's begin tic tac toe\n{game_board.__str__()}\n")
                        game_started = True
                        if game_started:
                            # print(f"turn: {turn}")
                            self.broadcast(f"[server]: It's your turn {turn}\n", whoTo=turn)

                # a message from a client, not a new connection
                else:
                    # Make sure there is enough players for each team and the board isn't filled
                    if self.check_for_players() and not self.game_board.board_full():
                    # process data recieved from client
                        try:
                            # receiving data from the socket.
                            data = read_sock.recv(4096).decode('UTF-8')
                            # print(f"after data recv else statement: {data}")
                            if data:
                                if game_started:
                                    if data[0] == '(':
                                        if self.players_sockets.get(read_sock.getpeername(), None)[1] == turn:
                                            """Check if the data from the person whose turn it is a move"""
                                            if self.sanitize_input(data, turn):
                                                self.broadcast(f"\n{game_board.__str__()}\n")

                                                if self.game_board.find_winner() is not None:
                                                    winner = self.game_board.find_winner()
                                                    self.broadcast(f"The winner is {winner}\nEnding server now\n")
                                                    return

                                                turn = 'O' if turn == 'X' else 'X'
                                                self.broadcast(f"It's your turn {turn}\n")
                                            else:
                                                self.broadcast(f"\r[{str(read_sock.getpeername())}]: {data}", sock=read_sock)
                                        else:
                                            self.broadcast(f"\r[{str(read_sock.getpeername())}]: {data}", sock=read_sock)
                                    else:
                                        self.broadcast(f"\r[{str(read_sock.getpeername())}]: {data}", sock=read_sock)

                            else:
                                # remove the socket that's broken
                                if read_sock in self.players_sockets:
                                    # print("Sock in else: {}".format(sock))
                                    # print(f"peer name: {read_sock.getpeername()}")
                                    self.players_sockets.pop(read_sock)

                                # at this stage, no data means probably the connection has been broken
                                self.broadcast(f"Client {addr} is offline\n")

                        except Exception as e:
                        # at this stage, no data means probably the connection has been broken
                            self.broadcast(f"Client {addr} is offline\n")
                            print(f"ERROR: {e}\n")
                            continue

                    else:
                        self.broadcast("There are not enough players to continue. Exiting now...\n")
                        game_started = False
                        return

    def broadcast(self, message: str, **kwargs: Dict):
        """Sends messages to players connected to the server

            Sends messages to players contained in the dictionary: players_sockets

            Args:
                message (str): Message to send out to player(s)
                **kwargs (Dict)
                    whoTo (str): Specifies who to send the message to
                    sock (Socket): Specifies the socket that sent the message

            Returns:
                None
                Sends message to players based on whoTo and sock

            Notes:
                whoTo = 'X' send to only X players (asking for move)
                whoTO = 'O' send to only O players (asking for move)
                whoTo = "self" send to player who just connected (tell player what their symbol is)
        """

        server_name = self.server_socket.getsockname()
        if 'sock' in kwargs:
            socket_sent_msg = kwargs['sock'].getpeername()
        else:
            socket_sent_msg = server_name

        for address in self.players_sockets:
            # send the message only to peer
            try:
                if 'whoTo' not in kwargs:
                    # Try sending to all sockets
                    if address not in (server_name, socket_sent_msg):
                        self.players_sockets[address][0].send(bytes(message, 'UTF-8'))
                else:
                    if kwargs['whoTo'] == 'X':
                        # Broadcast to only X players
                        if address not in (server_name, socket_sent_msg) and self.players_sockets[address][1] == 'X':
                            self.players_sockets[address][0].send(bytes(message, 'UTF-8'))
                    elif kwargs['whoTo'] == 'O':
                        # Broadcast to only O players
                        if address not in (server_name, socket_sent_msg) and self.players_sockets[address][1] == 'O':
                            self.players_sockets[address][0].send(bytes(message, 'UTF-8'))
                    elif kwargs['whoTo'] == "self":
                        # Broadcast to the player
                        if address == socket_sent_msg:
                            self.players_sockets[address][0].send(bytes(message, 'UTF-8'))

            except Exception as msg:
                self.players_sockets[address][0].close()

                # broken socket, remove it
                if address in self.players_sockets:
                    self.players_sockets.pop(address)
                print(f"\nERROR: {msg}\n")

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 9009
    SERVER = Server(HOST, PORT)

    try:
        SERVER.chat_server()
        SERVER.server_socket.close()

    except KeyboardInterrupt:
        SERVER.server_socket.close()
        print("\n")
        sys.exit()

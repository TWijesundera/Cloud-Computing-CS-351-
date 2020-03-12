"""P2P Client class

    This class calculates the most common words in a book
        and connects directly to another client instance

    Author: Thisara Wijesundera
    CS-351
    Assignment 4
"""

import os
import sys
import socket
import select
import itertools

from collections import Counter
from typing import List

class Client:

    def __init__(self, book_url: str):
        """Constructor for the Client class

            Args:
                book_url (str): Url the user input for book from gutenburg
            
            Instance Variables:
                self.most_common (Set): 50 most common words in downloaded book

            Returns:
                Client Object
        """
        try:
            self.most_common = self.most_frequent_words(book_url)
        except OSError as msg:
            print(msg)
            sys.exit()

    def most_frequent_words(self, book_url: str) -> List:
        """Generates a dict of the most frequent words

            Args:
                book_url (str): User provided book to get from gutenburg

            Returns:
                List (tuple): (<word>, <count>) a list of the 50 most common words and their count
        """
        if self.retrieve_book(book_url):
            book = []
            with open("book.txt", encoding='UTF-8') as f:
                for line in f:
                    split_line = [word for word in line.split() if len(word) >= 5 and word.isalpha() and word not in ("\n", " ")]
                    if len(split_line) > 0:
                        book.append(split_line)
            flat_list = list(itertools.chain(*book))
            frequent_50 = Counter(flat_list).most_common(50)
            return set([tup[0] for tup in frequent_50])
        else:
            raise OSError("Failed to retrieve book. Please check your internet connection\n")

    def retrieve_book(self, book_url: str) -> bool:
        """Gets a book from an author from the internet

            Args:
                book_url (str): url to wget book provided by user

            Returns:
                True: Book was retrieved
                False: Book was not retrieved

        """
        try:
            os.system(f"wget -O book.txt {book_url}")
            return True
        except OSError:
            return False

    def client_loop(self, HOST: str, PORT: str):
        """Method that connects to the torrent server

            Args:
                HOST (str): The ip address of the torrent server
                PORT (str): The port of the torrent server (changes to int)

            Returns:
                None (But it prints out to the user words that frequently show up in both books)

            Notes:
                First the program connects to the torrent server
                Once a connection is made the server tells the program to start a server
                    This only happens if its the first to connect
                    Otherwise the server tells the program what ip address and port to connecet to
                
                If a server was started then wait for a connection
                Once a connection is recieved then exhange the most common words found in the book
                    provided by the user

                Else
                    Connect to the ip address over the port provided and exchange information

            Variables:
                peer_flag (bool): Flag to tell if a the program was told to become a server
                cient_flag (bool): Flag to tell if the program was told to connect to a p2pServer
                direct_conn_info (List): Info of the server to connect to
        """

        peer_flag = False
        client_flag = False
        direct_conn_info = []

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(2)
        socket_list = [sys.stdin, client_socket]

        try:
            client_socket.connect((HOST, int(PORT)))
            
            while not peer_flag:
            # Get the list sockets which are readable
                ready_to_read, ready_to_write, in_error = select.select(socket_list , [], [])

                for sock in ready_to_read:             
                    if sock == client_socket:
                        # incoming message from remote server, s
                        data = sock.recv(4096).decode('UTF-8')
                        if not data:
                            print ("\nDisconnected from torrent server\n")
                            sys.exit()
                        else:
                            if data == "serverPeer":
                                peer_flag = True
                            elif data.split()[0].count('.') == 3:
                                direct_conn_info = data.split()
                                peer_flag = True
                                client_flag = True
                            else:
                                sys.stdout.write(f"{data.split()[0]}\n")
            
            # Now create a server socket and send the port back to the server
            if peer_flag and not client_flag:
                server = self.start_server()
                client_socket.send(bytes(f"{server.getsockname()[1]}", 'UTF-8'))
                exchange_info = False

                # Wait for a connection
                while not exchange_info:
                    client_sock, addr = server.accept()
                    print(f"Got a connection from {addr}")
                    client_sock.send(bytes("{}".format(" ".join(self.most_common)), 'UTF-8'))
                    common_from_client = client_sock.recv(4096).decode('UTF-8')
                    common_words = self.most_common.intersection(set(common_from_client.split()))
                    sys.stdout.write(f"\nThese words are common between the two books:\n{common_words}\n")
                    exchange_info = True
            
            elif client_flag:
                self.direct_connect(direct_conn_info)

        except socket.error as msg:
            print(msg)

    def start_server(self) -> object:
        """Server side code after client connects to server

            Returns:
                server_socket (Socket Object): Returns the socket that a
                    port and address are bound to

            Notes:
                This method is called after the program recieves instructions
                    to bind a server socket
                Happens after the client program is the first to connect
                    to the torrent server
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 9040))
        server_socket.listen(10)
        print("Started to listen on port 9040")
        return server_socket

    def direct_connect(self, info: List):
        """Client side code after second client connects

            Send the 50 most common words to the server
                the client directly connects to

            Args:
                info (List): A list that tells the method
                    what address and port to connect to
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        # Connect to server given from the torrent server
        s.connect((info[0], int(info[1])))
        s.send(bytes("{}".format(" ".join(self.most_common)), 'UTF-8'))
        data = s.recv(4096).decode('UTF-8')
        common_words = self.most_common.intersection(set(data.split()))
        sys.stdout.write(f"\nThese words are common between the two books:\n{common_words}\n")

if __name__ == "__main__":
    """Main method of the program
       
       Args:
            arg[1]: Host name of torrent server
            arg[2]: Port number of torrent server
            arg[3]: URL of book from guttenburg
                EX) http://www.gutenberg.org/files/863/863-0.txt
    """
    if len(sys.argv) != 4:
        print("Usage: python3 p2pClient.py <HOST> <PORT> <URL_to_book>\n")
        sys.exit()
    else:
        HOST = sys.argv[1]
        PORT = sys.argv[2]
        book_url = sys.argv[3]

    try:
        client = Client(book_url)
        client.client_loop(HOST, PORT)

    except KeyboardInterrupt:
        print("\n")
        sys.exit()

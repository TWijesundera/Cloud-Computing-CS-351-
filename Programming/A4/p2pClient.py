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

class Client:

    def __init__(self):
        """Constructor for the Client class

            Args:
                HOST: Host address
                PORT: Port to connect to
            
            Instance Variables:
                self.most_common (List[tuple]): 50 most common words in downloaded book
                self.bound_socket (Socket obj): Socket for connecting to server
                    Will change when recieves message from server

            Returns:
                Client Object
        """
        try:
            self.most_common = self.most_frequent_words()
        except socket.error as msg:
            print(f"Unable to bind socket\nERROR:{msg}\n")
            sys.exit()
        except OSError as msg:
            print(msg)
            sys.exit()

    def most_frequent_words(self):
        """Generates a dict of the most frequent words

            Args:

            Returns:
                List (tuple): (<word>, <count>) a list of the 50 most common words and their count
        """
        if self.retrieve_book():
            book = []
            with open("book.txt", encoding='utf-8') as f:
                for line in f:
                    split_line = [word for word in line.split() if len(word) >= 5 and word.isalpha() and word not in ("\n", " ")]
                    if len(split_line) > 0:
                        book.append(split_line)
            flat_list = list(itertools.chain(*book))
            return Counter(flat_list).most_common(50)
        else:
            raise OSError("Failed to retrieve book. Please check your internet connection\n")

    def retrieve_book(self) -> True:
        """Gets a book from an author from the internet

            Returns:
                True: Book was retrieved
                False: Book was not retrieved

            Notes:
                Might try making this more robust by allowing the user to
                query Gutenburg for author names and getting a
                random book?
        """
        try:
            os.system("wget -O book.txt http://www.gutenberg.org/files/863/863-0.txt")
            return True
        except OSError:
            return False

    def client_loop(self, HOST, PORT):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(2)
        peer_flag = False
        socket_list = [sys.stdin, client_socket]

        try:
            client_socket.connect((HOST, int(PORT)))
            
            while True:
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
                            #print data
                            if data == "serverPeer":
                                peer_flag = True
                                port_to_conn = self.start_server()
                                sys.stdout.write(data)

                    else:
                        # user entered a message
                        msg = sys.stdin.readline()
                        s.send(bytes(msg, 'UTF-8'))
        except socket.error as msg:
            print(msg)

    def start_server(self) -> int:
        pass

if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = sys.argv[2]

    try:
        client = Client()
        client.client_loop(HOST, PORT)

    except KeyboardInterrupt:
        print("\n")
        sys.exit()

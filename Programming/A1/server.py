# Server program to run on EC2
# CS 351
# Thisara Wijesundera

"""
    Description:
        This program is meant to recieve a file from the client
        and process the file
        The server will count the number of characters, words,
        and lines in the file and send it back to the client.

    Usage:
        python server.py <port_number>
    
    Returns:
        Sends number of characters, words, and lines to the client
"""

import socket
import sys


def sanitizePort(port_number: str) -> bool:
    """ Return bool if port number is less than 3 numbers """
    return len(port_number) > 3

def processFile() -> list:
    """Counts the number of lines, words, and charcters in a file

        Args:
            No value
        
        Returns:
            list[int]: [number of lines, number of words, number of characters]
                        contained in 'countfile'
        
        Todo:
            Instead use the recieved buffer to modify without creating/reading
                from count file
        
    """
    num_chars = 0
    num_words = 0

    with open("./countfile", 'rb') as f:
        """Count the number of words, lines, and charaters for every line in file
            
            Note:
                'line_num' is 0 based (becuase of enumerate), therefore must add 1 when returning
                Adding the count of spaces and '\n' characters which are stripped during 'line.split'
        """


        for line_num, line in enumerate(f):
            words = line.split() # Words in line (List[str])
            # print(words)
            num_words += len(words)
            # Generator function which calculates the sum of all words in a line
            # print([word for word in words])
            num_chars += sum(len(word) for word in words) + line.count(b' ')+ line.count(b'\n')
    
    return [line_num+1, num_words, num_chars]
    
    
if __name__ == "__main__":
    # Get local machine name
    try:
        if len(sys.argv) != 2:
            raise Exception("\nMake sure you are running the program correctly. " \
            "python3 server.py <port_number>\n")
    
    # Create a socket object
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        if sanitizePort(sys.argv[1]):
            port = int(sys.argv[1])
        else:
            raise Exception("\nPlease choose a higher port number\n")
    except Exception as e:
        print(e)
        quit()

    # Bind to port
    server_sock.bind((host, port))

    # Queue up to 5 requests
    server_sock.listen(5)

    try:
        """
            While True to keep server available to take connections from clients
        """
        while True:
            infile = open('./countfile', 'wb')
            # Establish connection
            client_sock, addr = server_sock.accept()

            rec = client_sock.recv(4096)
            while(rec):
                infile.write(rec)
                rec = client_sock.recv(4096)

            infile.close()

            print("Got a connection from {}".format(str(addr)))

            counts = processFile()
            # print(counts)

            msg = "Hostname: {} \n Port: {} \n Number of lines: {} \
                    \n Number of words: {} \n Number of characters: {} \r\n" \
                    .format(host, port, counts[0], counts[1], counts[2])

            client_sock.sendall(msg.encode('ascii'))
            client_sock.close()

    except KeyboardInterrupt:
        print("\n")
        server_sock.close()

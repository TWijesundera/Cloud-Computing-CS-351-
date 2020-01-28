"""
    Server program to run on EC2
    CS 351
    Thisara Wijesundera

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

def sanitizePort(port_number):
	return len(port_number) > 3

def processFile ():
    num_chars = 0
    num_words = 0

    with open("./countfile", 'r') as file:
        """
            Write comment for loop here
        """
        for line_num, line in enumerate(file):
            words = line.split()
            num_words += len(words)
            num_chars += sum(len(word) for word in words)

    # Must add the length of "words" because they were split by spaces
    return [line_num+1, num_words, num_chars+len(words)]
    
if __name__ == "__main__":
    # Create a socket object
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    try:
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
            Write comment for loop
        """
        while True:
            infile = open('./countfile', 'wb')
            # Establish connection
            client_sock, addr = server_sock.accept()

            rec = client_sock.recv(4096)
            while(rec):
                infile.write(rec)
                rec = client_sock.recv(4096)

            print("Got a connection from {}".format(str(addr)))

            counts = processFile()
            print(counts)

            msg = "Hostname: {} \n Port: {} \n Number of lines: {} \
            \n Number of words: {} \n Number of characters: {} \r\n".format(host, port, counts[0], counts[1], counts[2])
            client_sock.sendall(msg.encode('ascii'))
            client_sock.close()

    except KeyboardInterrupt:
        print("\n")
        server_sock.close()


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
        python server.py
    
    Returns:
        Sends number of characters, words, and lines to the client
"""
import socket


def processFile ():
    num_chars = 0
    num_words = 0

    with open("./countfile", 'r') as file:
        for line_num, line in enumerate(file):
            words = line.split()
            num_words += len(words)
            num_chars += sum(len(word) for word in words)
    file.close()

    return [line_num+1, num_words, num_chars+len(words)]
    
if __name__ == "__main__":
    # Create a socket object
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = socket.gethostname()
    port = 34590

    # Bind to port
    server_sock.bind((host, port))

    # Queue up to 5 requests
    server_sock.listen(5)

    infile = open('./countfile', 'wb')

    try:
        while True:
            # Establish connection
            client_sock, addr = server_sock.accept()

            rec = client_sock.recv(1024)
            while(rec):
                infile.write(rec)
                rec = client_sock.recv(1024)

            infile.close()

            print("Got a connection from {}".format(str(addr)))

            counts = processFile()
            print(counts)

            msg = "The hostname is: {} \n Number of line: {} \
            \n Number of words: {} \n Number of characters: {} \r\n".format(host, counts[0], counts[1], counts[2])
            client_sock.send(msg.encode('ascii'))
            client_sock.close()

    except KeyboardInterrupt:
        server_sock.close()


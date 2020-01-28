"""
    Thisara Wijesundera
    CS 351
    Assignment 1: client.py

    Description:
        This program is meant to recieve number or characters,
        words, and lines in the file sent to the server

    Usage:
        python client.py <server_ip_address> <port_number> <path_to_file>
        
        <path_to_file> should be a text file???

    Returns:
        hostname, port
        filename = {} number of characters, {} number of words, {} number of lines
"""
import socket
import sys

def sanitizeIP(ip_address):
	return ip_address.count('.') == 3

def sanitizePort(port_number):
	return len(port_number) > 3


if __name__  == "__main__":
    try:
        if len(sys.argv) != 4:
            raise Exception("\nMake sure you are running the program correctly " \
            "python client.py <server_ip> <port_number> <file_path>\n")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
        if sanitizeIP(sys.argv[1]):
            host = sys.argv[1]
        else:
            raise Exception("\nPlease make sure the IP address is correct\n")
        
        if sanitizePort(sys.argv[2]):
            port = int(sys.argv[2])
        else:
            raise Exception("\nPlease choose a higher port number\n")

        s.connect((host, port))
    except Exception as e:
        print(e)

    file_to_send = open(sys.argv[3], 'rb')
    transmit = file_to_send.read(4096)

    while transmit:
        s.sendall(transmit)
        transmit = file_to_send.read(4096)

    s.shutdown(socket.SHUT_WR)

    # Recieve no more than 4096 bytes
    msg = s.recv(1024)
    s.close()
    print(msg.decode('ascii'))

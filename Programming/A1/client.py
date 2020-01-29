# Thisara Wijesundera
# CS 351
# Assignment 1: client.py

"""
    MUST BE RUN USING PYTHON3

    Description:
        This program is meant to recieve number or characters,
        words, and lines in the file sent to the server

    Usage:
        python3 client.py <server_ip_address> <port_number> <path_to_file>
        
        <path_to_file> should be a text file???

    Returns:
        hostname, port
        filename = {} number of characters, {} number of words, {} number of lines
"""

import socket
import sys
import os

def sanitize_ip(ip_address: str) -> bool:
    """ Return bool if ip_address has 3 periods """
    return ip_address.count('.') == 3

def sanitize_port(port_number: str) -> bool:
    """ Return bool if port number is less than 3 numbers """
    return len(port_number) > 3

def check_file_size(file_path: str) -> bool:
    """ Return bool if file size is greater than 4096 bytes """
    return os.stat(file_path).st_size > 4096


if __name__  == "__main__":
    try:
        if len(sys.argv) != 4:
            raise Exception("\nMake sure you are running the program correctly " \
            "python3 client.py <server_ip> <port_number> <file_path>\n")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
        if sanitize_ip(sys.argv[1]):
            host = sys.argv[1]
        else:
            raise Exception("\nPlease make sure the IP address is correct\n")
        
        if sanitize_port(sys.argv[2]):
            port = int(sys.argv[2])
        else:
            raise Exception("\nPlease choose a higher port number\n")
        
        if not check_file_size(sys.argv[3]):
            f = sys.argv[3]
        else:
            raise Exception("\nFile size is too large. Please pick a different file\n")

        s.connect((host, port))
        
        file_to_send = open(f, 'rb')
        transmit = file_to_send.read(4096)

        """
            While there is data in the file
            transmit the data and read again
        """
        while transmit:
            s.sendall(transmit)
            transmit = file_to_send.read(4096)

        s.shutdown(socket.SHUT_WR)

        # Recieve no more than 4096 bytes
        msg = s.recv(4096)
        s.close()
        print(msg.decode('ascii'))

    except Exception as e:
        print(e)



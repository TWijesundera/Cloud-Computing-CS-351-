"""
    Client program to run on EC2 server
    CS 351
    Thisara Wijesundera

    Description:
        This program is meant to recieve number or characters,
        words, and lines in the file sent to the server

    Usage:
        python client.py <server_ip_address> <path_to_file>
        
        <path_to_file> should be a text file???

    Returns:
        hostname, port
        filename = {} number of characters, {} number of words, {} number of lines
"""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()
port = 9999

# Connection to hostname on port
s.connect((host, port))

file_to_send = open('./smallSample.txt', 'rb')
transmit = file_to_send.read(1024)

while transmit:
    s.sendall(transmit)
    transmit = file_to_send.read(1024)

s.shutdown(socket.SHUT_WR)

#Recieve no more than 1024 bytes
msg = s.recv(1024)
s.close()
print(msg.decode('ascii'))
"""
	Client side code from tutorial point
	CS 351
	Thisara Wijesundera
"""

import socket

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()
port = 9999

# Connection to hostname on port
s.connect((host, port))

#Recieve no more than 1024 bytes
msg = s.recv(1024)
s.close()
print(msg.decode('ascii'))
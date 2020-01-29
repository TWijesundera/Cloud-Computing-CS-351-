# CS 351
# Thisara Wijesundera
# Tutorial points Python simple server code

import socket

# Create a socket object
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()
port = 9999

# Bind to port
server_sock.bind((host, port))

# Queue up to 5 requests
server_sock.listen(5)

while True:
	# Establish connection
	client_sock, addr = server_sock.accept()
	
	print("Got a connection from {}".format(str(addr)))
	
	msg = "Thank you for connecting" + "\r\n"
	client_sock.send(msg.encode('ascii'))
	client_sock.close()
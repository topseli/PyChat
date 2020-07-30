#!/usr/bin/python
"""
@author: topseli

original author Deepak Srivatsav https://www.geeksforgeeks.org/simple-chat-room-using-python
"""

import socket
import select
import sys
from PyQt5 import QtWidgets, uic

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Naive input check that the user provided enough command line parameters
if len(sys.argv) != 3:
	print("Provide PyChat with an ip address and a port number for the server")
	print("ie python PyChat 192.168.1.2 65000")
	exit()

# Set the parameters as ip address and por
IP_address = str(sys.argv[1])
port = int(sys.argv[2])

# "Try to connect to the address and port"
try:
	server.connect((IP_address, port))
	print("Connected to a PyChat server at " + IP_address)
except:
	print("No server found at " + IP_address + " listening to the port " + str(port))
	exit()



# The main loop!
while True:

	socketList = [sys.stdin, server]

	read_sockets, write_socket, error_socket = select.select(socketList,[],[])

	for socket in read_sockets:
		if socket == server:
			message = socket.recv(2048)
			print(message)
		else:
			message = sys.stdin.readline()
			server.send(message)
			sys.stdout.write("<You>" + message + "\n")
			sys.stdout.flush()
server.close

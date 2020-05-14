#!/usr/bin/python

"""
@author: topseli

original author Deepak Srivatsav https://www.geeksforgeeks.org/simple-chat-room-using-python
"""

import socket
import select
import sys
from _thread import *

version = "0.1"

"""AF_INET is the ip address for the socket, SOCK_STREAM is the socket type -->
data/characters are read in a continuous flow"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("This is PyChat server software version " + version)
print("listening to the TCP port " + sys.argv[2] + " for connections at " + sys.argv[1])

#Check that the user provided enough parameters

if len(sys.argv) != 3:
	print("You need to provide PyChatSrv with an ip address and a port number")
	print("ie. python PyChatSrv.py 192.168.1.2 65000")
	exit()

#Should be sanitized?
"""
if type(sys.argv[2]) != int:
	print("Input an integer as the port number")
	exit()
	
	
	0 < port < 655554
	ETC ETC....
"""

#Set the ip address to localhost and the prompt argument as the port number
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

#binds the server to the ip address and port number
#Is this a tuple?
server.bind((IP_address, Port))

#set the server to listen to 20 connections
#can be increaser
server.listen(20)

#initialize a list to hold the clients
clients = []

"""Listens for messages from the clients and calls the broadcast function that
sends the message to every client"""
def clientThread(conn, addr):
	#Greet new clients
	conn.send("Welcome to PyChat. The server is running PyChat version " + version)
	
	while True:
		try:
			message = conn.recv(2048)
			if message:
				user_and_message = "<" + addr[0] + "> " + message
				
				#Print the user's address and the message on the server terminal
				#Then broadcast the message to the clients
				print(user_and_message)
				broadcast(user_and_message, conn)
			
			#if the message has no content the connection is propably broken
			#so we remove it
			else:
				remove(conn)
		
		except:
			continue

#Broadcasts the users message to other clients
def broadcast(message, connection):
	for client in clients:
		if client!=connection:
			try:
				client.send(message)
			except:
				client.close()
				
				#if the link is broken remove the client from the list
				remove(client)

#for removing clients from the list
def remove(connection):
	if connection in clients:
		clients.remove(connection)

#The main loop!
while True:
	"""
	Accepts a connection request from a client and stores the users socket object as conn 
	and the users ip addres as addr"""
	conn, addr = server.accept()
	
	#Maintain a list of active connections for broadcasting
	clients.append(conn)
	
	#Print the address of every new connection to the server terminal
	print(addr[0] + " connected")
	
	"Start a new thread for every client"
	start_new_thread(clientThread,(conn,addr))
	
conn.close()
server.close

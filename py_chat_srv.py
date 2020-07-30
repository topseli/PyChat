#!/usr/bin/python

"""
@author: topseli

original author Deepak Srivatsav https://www.geeksforgeeks.org/simple-chat-room-using-python
"""

import socket
import sys
import threading

version = "0.1"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("This is PyChat server software version " + version)
print("listening to the TCP port " + sys.argv[2] + " for connections at " + sys.argv[1])

# A naive check that the user provided enough parameters

if len(sys.argv) != 3:
    print("You need to provide PyChatSrv with an ip address and a port number")
    print("ie. python PyChatSrv.py 192.168.1.2 65000")
    exit()

# Should be sanitized?
"""
if type(sys.argv[2]) != int:
    print("Input an integer as the port number")
    exit()


    0 < port < 655554
    ETC ETC....
"""

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(20)
clients = []


def clientThread(conn, addr):

    # Greet new clients
    conn.send(
        "Welcome to PyChat. The server is running PyChat version " + version)

    while True:
        try:
            message = conn.recv(2048)
            if message:
                user_and_message = "<" + addr[0] + "> " + message
                print(user_and_message)
                broadcast(user_and_message, conn)
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()
            remove(client)


def remove(connection):
    if connection in clients:
        clients.remove(connection)


while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(addr[0] + " connected")
    start_new_thread(clientThread, (conn, addr))

conn.close()
server.close

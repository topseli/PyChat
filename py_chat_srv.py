#!/usr/bin/python

"""
@author: topseli

original author Deepak Srivatsav
https://www.geeksforgeeks.org/simple-chat-room-using-python
"""

import socket
import sys
import threading

version = "0.1"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 2:
    print("You need to provide PyChatSrv with an ip address.")
    print("'python3 py_chat_srv.py localhost'")
    exit()

IP_address = str(sys.argv[1])
Port = 42069

print("This is PyChat server software version " + version)
print("listening to the TCP port " + str(Port) + " for connections at "
      + IP_address)

server.bind((IP_address, Port))
server.listen(20)
client_sockets = []


def clientThread(name, conn):
    username = conn.recv(2048).decode("utf-8")
    print(username + " connected")
    conn.send(
        ("Welcome to PyChat. The server is running PyChat version " + version).encode("utf-8"))

    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                user_and_message = "<" + username + "> " + message
                print(user_and_message)
                broadcast(user_and_message, conn)
            else:
                remove(conn)
                continue
        except Exception as e:
            print(e)
            continue

        
def broadcast(message, connection):
    for client in client_sockets:
        if client != connection:
            try:
                client.send(message)
            except Exception:
                client.close()
            remove(client)


def remove(connection):
    if connection in client_sockets:
        client_sockets.remove(connection)


while True:
    conn, addr = server.accept()
    client_sockets.append(conn)
    thread = threading.Thread(target=clientThread, args=(1, conn))
    thread.start()
    thread.join()

conn.close()
server.close

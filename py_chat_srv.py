#!/usr/bin/python

"""
@author: topseli

original author Deepak Srivatsav
https://www.geeksforgeeks.org/simple-chat-room-using-python
"""

import socket
import sys
import threading
import logging

version = "0.1"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 2:
    logging.error("You need to provide PyChatSrv with an ip address.")
    logging.error("'python3 py_chat_srv.py localhost'")
    exit()

IP_address = str(sys.argv[1])
Port = 42069

logging.info("This is PyChat server software version " + version)
logging.info("Server is running at %s:%s", IP_address, str(Port))

server.bind((IP_address, Port))
server.listen(20)
client_sockets = []


def client_thread(id, conn):

    conn.send(
        ("Welcome to PyChat. The server is running PyChat version "
         + version).encode("utf-8"))

    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                user_and_message = ("<" + username + "> " + message)
                logging.info(user_and_message)
                broadcast(user_and_message, conn)
            else:
                remove(conn)
                return
        except Exception as e:
            print(e)
            continue


def broadcast(message, conn):
    for client in client_sockets:
        try:
            client.send(message.encode("utf-8"))
        except Exception:
            client.close()
            client.remove(conn)


def remove(conn):
    if conn in client_sockets:
        client_sockets.remove(conn)


while True:
    conn, addr = server.accept()
    client_sockets.append(conn)
    username = conn.recv(2048).decode("utf-8")
    logging.info("<%s> connected!", username)
    broadcast
    threading.Thread(target=client_thread, args=(1, conn)).start()

conn.close()
server.close

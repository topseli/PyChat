#!/usr/bin/python

"""
@author: topseli

original author Deepak Srivatsav
https://www.geeksforgeeks.org/simple-chat-room-using-python
"""

import socket
import sys
import threading
import base64
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
Port = 21012

logging.info("This is PyChat server software version " + version)
logging.info("The Server is running at %s:%s", IP_address, str(Port))

server.bind((IP_address, Port))
server.listen(20)
client_sockets = []


def to_base64(message):
    return base64.encodebytes(message.encode("utf-8"))


def rcv_base64(message):
    return base64.decodebytes(message).decode("utf-8")


def client_thread(id, conn):
    username = rcv_base64(conn.recv(2048))
    logging.info("<%s> connected.", username)
    conn.send(
        to_base64("Welcome to PyChat. The server is running PyChat version " + version + "\n"))

    broadcast("<" + username + "> connected.", conn)

    while True:
        try:
            message = rcv_base64(conn.recv(2048))
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
            client.send(to_base64(message))
        except Exception:
            client.close()
            remove(conn)


def remove(conn):
    if conn in client_sockets:
        client_sockets.remove(conn)


while True:
    conn, addr = server.accept()
    client_sockets.append(conn)
    threading.Thread(target=client_thread, args=(1, conn)).start()

conn.close()
server.close

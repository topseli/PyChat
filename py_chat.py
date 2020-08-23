# -*- coding: utf-8 -*-
""" py_chat.py - Main class for a simple chat program"""
__author__ = "topseli"
__credits__ = ["Deepak Sritvatsav"]
__license__ = "0BSD"

import sys
import os
import socket
# import select
from PyQt5 import QtWidgets, uic

import login_view
import chat_view


class PyChat(QtWidgets.QWidget):

    def __init__(self):
        super(PyChat, self).__init__()
        self.init_ui()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/main_window.ui'
        uic.loadUi(path, self)

        # Create QWidget instances
        self.login_widget = login_view.LoginView()
        self.chat_widget = chat_view.ChatView()

        # Add QWidget instances to stackedWidget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.chat_widget)

        # Connect exit_buttons
        self.login_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)
        self.chat_widget.exit_button.clicked.connect(
            self.on_exit_button_clicked)

        # Connect signals
        self.login_widget.login_signal.connect(
            self.on_login_clicked)
        self.chat_widget.send_signal.connect(
            self.on_send_clicked)

    def on_exit_button_clicked(self):
        sys.exit(0)

    def on_login_clicked(self, login_info):
        print(login_info)
        try:
            self.server.connect((login_info["address"], login_info["port"]))
            self.server.sendall(login_info["username"].encode("utf-8"))
            welcome_msg = self.server.recv(2048)
        except ConnectionRefusedError as e:
            print("Connection Refused Error: " + str(e))
            # TODO : Open a QMessageBox displaying the error
            return

        self.chat_widget.chat_display.insertPlainText(welcome_msg.decode("utf-8"))
        self.stacked_widget.setCurrentWidget(self.chat_widget)

    def on_send_clicked(self, message):
        self.server.sendall(message.encode("utf-8"))


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = PyChat()
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()

# -*- coding: utf-8 -*-
""" chat_view.py - presenter for the chat"""
__author__ = "topseli"
__license__ = "0BSD"

import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class ChatView(QtWidgets.QWidget):

    send_signal = pyqtSignal()

    def __init__(self):
        super(ChatView, self).__init__()
        self.init_ui()

    def init_ui(self):
        path = os.path.dirname(os.path.abspath(__file__)) + '/chat_view.ui'
        uic.loadUi(path, self)

    @pyqtSlot()
    def on_send_button_clicked(self):
        self.send_signal.emit()


def run():
    APP = QtWidgets.QApplication(sys.argv)
    APP_WINDOW = ChatView()
    APP_WINDOW.exit_button.clicked.connect(sys.exit)
    APP_WINDOW.show()
    APP.exec_()


if __name__ == '__main__':
    run()

from multiprocessing.connection import Listener
from threading import Thread
from collections import deque

from plugins.nvda.src.commConstants import address, authkey


class _OutputServer:
    def __init__(self):
        self.__connectToClient()

    def __connectToClient(self):
        self.__connection = None
        Thread(target=self.__waitForClientToConnect, daemon=True).start()

    def __waitForClientToConnect(self):
        listener = Listener(address, authkey=authkey)
        self.__connection = (
            listener.accept()
        )  # this is blocking until a client connects

        self.__sendAllUnsentMessages()

    def send(self, msg):
        if self.__connection:
            try:
                self.__connection.send(msg)

            except ConnectionResetError:  # If the native app is terminated
                self.__connectToClient()  # In case it restarts
        else:
            self.__recordUnsentMessage(msg)

    def __recordUnsentMessage(self, msg):
        try:
            self.__unsentMsgs
        except AttributeError:
            self.__unsentMsgs = deque()

        self.__unsentMsgs.append(msg)

    def __sendAllUnsentMessages(self):
        if self.__unsentMsgs:
            while self.__unsentMsgs:
                msg = self.__unsentMsgs.popleft()
                self.send(msg)


def startOutputServer():
    return _OutputServer()

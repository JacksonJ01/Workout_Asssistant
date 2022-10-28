# from time import sleep as s
# from threading import Timer
from socket import socket, AF_INET, \
    SOCK_DGRAM, SOCK_STREAM, gethostname as ghn, gethostbyname as gbhn

KEY = "Client"
HEADER = 160
HOSTNAME = gbhn(ghn())
PORT_NUMBER = 54124
SERVER_ADDRESS_PORT = (HOSTNAME, PORT_NUMBER)
FORMAT = "utf-8"
DISCONNECTING_MESSAGE = "Disconnecting"


def connect():
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(SERVER_ADDRESS_PORT)
        return client
    except ConnectionRefusedError:
        exit()


# client = connect()


class ClientMessaging():
    def __init__(self, key=KEY, header=HEADER, host=HOSTNAME, portNum=PORT_NUMBER,
                 serverPort=SERVER_ADDRESS_PORT, format=FORMAT,
                 dcMessage=DISCONNECTING_MESSAGE):
        self.key = key
        self.header = header
        self.host = host
        self.portNum = portNum
        self.serverPort = serverPort
        self.format = format
        self.dcMessage = dcMessage
        return

    @staticmethod
    def receiveServerMessage():
        try:
            client = connect()
            msg = (client.recv(HEADER).decode(FORMAT))
            return msg
        except IndexError:
            return None

    @staticmethod
    def sendServerMessage(msg: str):
        try:
            message = msg.encode(FORMAT)
            msgLength = len(message)
            sendLength = str(msgLength).encode(FORMAT)
            sendLength += b" " * (HEADER - len(sendLength))
            try:
                client = connect()
                client.send(sendLength)
                client.send(message)
            except ConnectionAbortedError:
                pass

        except ConnectionResetError:
            exit("Connection Could Not Be Made")

    def communicationLine(self):
        return

    def whom(self):
        return self.key


# Client1 = ClientMessaging
# while True:
#     Client1.sendServerMessage(input("Your Message>>>"))

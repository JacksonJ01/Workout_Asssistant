from time import sleep as s
from threading import Timer
from socket import socket, AF_INET,\
    SOCK_DGRAM, SOCK_STREAM, gethostname as ghn, gethostbyname as gbhn
from speechMain import chatBot

HEADER = 160
HOSTNAME = gbhn(ghn())
PORT_NUMBER = 54124
SERVER_ADDRESS_PORT = (HOSTNAME, PORT_NUMBER)
FORMAT = "utf-8"
DISCONNECTING_MESSAGE = "Disconnecting"

try:
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(SERVER_ADDRESS_PORT)
except ConnectionRefusedError:
    exit()

KEY = "Client1"


def receiveServerMessage(print_Message=False):
    try:
        msg = (client.recv(HEADER).decode(FORMAT))

        if ">" in msg and KEY in msg:
            for x in msg:
                if x == ">":
                    msg = msg.replace(">>> ", "")
                    break
                msg = msg[1:]
            # print(msg.replace("Server>>> ", ""))
            return msg, False

        if KEY in msg:
            return None, True
        elif print_Message is True:
            # print(msg, "\n")
            return msg, False

    except ConnectionAbortedError:
        return None, False


def sendServerMessage(msg, whom):
    _message = msg

    try:
        for _msg in range(2):
            if _msg == 0:
                msg = f"TO: {whom} | FROM: {KEY}"
            else:
                msg = f"KEY: {KEY}>>> {_message}"

            message = msg.encode(FORMAT)
            msgLength = len(message)
            sendLength = str(msgLength).encode(FORMAT)
            sendLength += b" " * (HEADER - len(sendLength))
            try:
                client.send(sendLength)
                # print(message)
                client.send(message)
            except ConnectionAbortedError:
                pass

    except ConnectionResetError:
        exit("Connection Could Not Be Made")


who = "Server"
speakingTo = []
try:
    # sendServerMessage(f"{DISCONNECTING_MESSAGE} | {KEY}", who)
    sendServerMessage("Connecting", who)
    printMessage = False
    while True:
        try:
            toSend = chatBot().strip()
            print(toSend)
            if toSend == DISCONNECTING_MESSAGE:
                break

            sendServerMessage(toSend, who)
            msg, printMessage = receiveServerMessage(printMessage)

            if printMessage is False:
                print(f"{who}>>> {msg}\n")
            elif printMessage is True:
                pass

                # s(2)
                # sendServerMessage(f"{DISCONNECTING_MESSAGE}", who)
            # print(printMessage)
        except TypeError:
            pass
finally:
    sendServerMessage(f"{DISCONNECTING_MESSAGE} | {KEY}", who)
    exit("Successfully Disconnected")
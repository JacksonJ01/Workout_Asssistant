from cameraMain import exerciseCamera
# from plotMain import plot
import keyboard
from time import sleep as s
from socket import socket, AF_INET,\
    SOCK_DGRAM, SOCK_STREAM, gethostname as ghn, gethostbyname as gbhn
from threading import Thread, active_count

# # Communication For Unity
# ipAddress = "127.0.0.1"
# portNumber = 54124
# server = socket(AF_INET, SOCK_DGRAM)
# serverAddressPort = (ipAddress, portNumber)
#
# while True:
#     allLocations = exerciseCamera()


# ______________________________________________________
# HandTracking.cs


# ______________________________________________________
# LineCode.cs
# using System.Collections;
# using System.Collections.Generic;
# using UnityEngine;
#
# public class LineCode : MonoBehaviour
# {
#
#     LineRenderer lineRenderer;
#
#     public Transform origin;
#     public Transform destination;
#
#     // Start is called before the first frame update
#     void Start()
#     {
#         lineRenderer = GetComponent<LineRenderer>();
#         lineRenderer.startWidth = 0.1f;
#         lineRenderer.endWidth = 0.1f;
#     }
#
#     // Update is called once per frame
#     void Update()
#     {
#         lineRenderer.SetPosition(0, origin.position);
#         lineRenderer.SetPosition(1, destination.position);
#     }
# }

# For this weeks exercise Friday, we are going to be using the
# Shoulder Press machine.

# We want to start off by adjusting the seat until were are at a comfortable height.
# Generally speaking, your shoulders should be around the height of the handles, not above them,
# and your fingers should be centered

# When used properly, this is a great exercise to target your:
# Deltoids
# Pectorals
# Triceps
# and mid to upper back muscles like your Trapezius

# The shoulder press machine is also helpful for single arm shoulder presses, which engages core muscles like your obliques.
# During each rep you have more load to either side and must correct for that using those muscles.

# In addition to that, it's a safe way add weight to your should press workout without having lift dumbbells or
# a barbell up and over your head.
#
#
#

KEY = "Server"
HEADER = 160
HOSTNAME = gbhn(ghn())
PORT_NUMBER = 54124
SERVER_ADDRESS_PORT = (HOSTNAME, PORT_NUMBER)
FORMAT = "utf-8"
DISCONNECTING_MESSAGE = "Disconnecting"
server = socket(AF_INET, SOCK_STREAM)
server.bind(SERVER_ADDRESS_PORT)


def ReceiveClientMessage(connection, address=None):
    connected = True
    while connected:
        try:
            msgLength = connection.recv(HEADER).decode(FORMAT)
            # print("1", msgLength)
            if msgLength:
                msgLength = int(msgLength)
                msg = connection.recv(msgLength).decode(FORMAT)

                # print("here 1", msg)
                if DISCONNECTING_MESSAGE in msg:
                    msg = msg.replace("KEY: ", "")
                    print(msg)
                    msg = msg.replace(">>>", "").replace(DISCONNECTING_MESSAGE, "").strip()
                    try:
                        # print(clients)
                        clients.remove(msg)
                        print(msg, "Removed\nS")
                    except ValueError:
                        # print("Failed", msg)
                        pass
                    connected = False
                    connection.close()

                if "TO: " in msg:
                    msg = f"{msg}".replace("TO: ", "")
                    destination = ""
                    for letter in msg:
                        if letter != " ":
                            destination += letter
                            msg = msg[1:]
                        else:
                            msg = msg.replace(" | FROM: ", "")
                            break

                    if destination == KEY:
                        try:
                            old = speakingTo[0]
                            if msg != old:
                                print("")
                        except IndexError:
                            pass
                        finally:
                            speakingTo.insert(0, msg)  # Might Cause Problems

                        if msg not in clients:
                            print(f"New Connection Between {speakingTo[0]}")
                            sendClientMessage(connection, "Connected", speakingTo[0])
                            # s(4)
                            # sendClientMessage(connection, "Test", speakingTo[0])
                            clients.append(msg)
                            # print(clients)
                            # print(f"{com} |" for com in clients)
                        else:
                            pass
                    else:
                        return

                elif "KEY: " in msg:
                    msg = msg.replace("KEY: ", "")
                    key = ""
                    for letter in msg:
                        if letter != ">":
                            key += letter
                        else:
                            break

                    if key == speakingTo[0]:
                        # print("2", msg)
                        sendClientMessage(connection, "Received", speakingTo[0])
                        print(msg.strip())

        except ConnectionResetError:
            pass


def sendClientMessage(connection, msg, toClient):
    message = msg
    for _message in range(2):
        if _message == 0:
            msg = f"TO: {toClient} | FROM: Server"
        else:
            msg = f"{KEY}>>> {message}"

        msg = msg.encode(FORMAT)
        msgLength = len(msg)
        sendLength = str(msgLength).encode(FORMAT)
        sendLength += b" " * (HEADER - len(sendLength))
        # print(msg)
        try:
            connection.send(msg)
        except ConnectionResetError:
            try:
                clients.remove(toClient)
            except ValueError:
                pass


def startServer():
    server.listen()
    print(f"Listening ON {HOSTNAME}\n")
    serverConnections = 1
    while True:
        connection, address = server.accept()
        thread = Thread(target=ReceiveClientMessage, args=(connection, address))
        thread.start()
        # print(f"\nActive Connections: {active_count() - serverConnections}\n")
        s(.25)


print("Starting Server")
clients = []
speakingTo = []
# startServer()

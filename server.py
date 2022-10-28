# from cameraMain import exerciseCamera
# from plotMain import plot
import keyboard
from time import sleep as s
from socket import socket, AF_INET,\
    SOCK_DGRAM, SOCK_STREAM, gethostname as ghn, gethostbyname as gbhn
from threading import Thread, active_count
from multiprocessing import Process, Manager
from timerStopwatch import timer

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


def ReceiveClientMessage(connection):
    connected = True
    while connected:
        try:
            msgLength = connection.recv(HEADER).decode(FORMAT)
            if msgLength:
                msgLength = int(msgLength)
                msg = connection.recv(msgLength).decode(FORMAT)
                if DISCONNECTING_MESSAGE in msg:
                    print(msg)
                    try:
                        clients.remove(msg)
                        print(msg, "Removed\n")
                    except ValueError:
                        pass
                    connected = False
                    connection.close()
                else:
                    msg = msg.strip()
                    msg = msg.lower()
                    msg = checkClientMessage(msg)
                    if "timer done" == msg:
                        print("Timer Done")
                    # if msg is not None:
                    #     print(msg, "\n")

        except ConnectionResetError:
            pass


def checkClientMessage(msg: str):
    if "starting timer for" in msg.lower():
        manager = Manager()
        global currentTimerTime
        currentTimerTime = manager.dict()

        global startTimer
        amountOfTime = [int(num) for num in msg.split() if num.isdigit()][0]

        if "seconds" in msg:
            startTimer = Process(target=timer, args=([0, 0, amountOfTime], currentTimerTime))
            unit = "seconds"
        elif "minutes" in msg:
            startTimer = Process(target=timer, args=([0, amountOfTime, 0], currentTimerTime))
            unit = "minutes"
        elif "hours" in msg:
            startTimer = Process(target=timer, args=([amountOfTime, 0, 0], currentTimerTime))
            unit = "hours"

        startTimer.start()
        # startTimer.join()

    elif "pausing timer" in msg.lower():
        # If user tries to pause the timer, the
        try:
            startTimer.terminate()
            currentTimerTime = currentTimerTime.values()
            print("Timer Paused At:", currentTimerTime)

        except AttributeError:
            pass

    else:
        return msg

    return None


def sendClientMessage(connection, msg: str, toClient):
    msg = msg.encode(FORMAT)
    msgLength = len(msg)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b" " * (HEADER - len(sendLength))
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
    while True:
        connection, address = server.accept()
        thread = Thread(target=ReceiveClientMessage, args=(connection,))
        thread.start()
        # threading
        # print(f"\nActive Connections: {active_count() - serverConnections}\n")
        s(.25)


currentTimerTime = 0
startTimer = None
print("Starting Server")
clients = []
speakingTo = []
startServer()

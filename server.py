from cameraMain import exerciseCamera
# from plotMain import plot
# import keyboard
from time import sleep as s
# from socket import socket, AF_INET,\
#     SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR,\
#     gethostname as ghn, gethostbyname as gbhn
from threading import Thread
from multiprocessing import Queue
# from timerStopwatch import timer
from time import time as t
from speechFunct import analyzeResponse


def passTime():
    global waitingForInput
    aTime = int(t())
    count = 3
    while waitingForInput:
        s(.1)
        # if timerActive is True:
        #     pass
        #
        # if int(t()) - aTime >= 3:
        #     aTime = int(t())
        #     print("Okay")


def chatBot(msg: Queue = None):
    userInput = input("Type your Message:\n>>>")

    _msg = msg.get()
    _msg["Message"] = userInput
    msg.put(_msg)


message = {"Message": "Okay"}
waitingForInput = True
timerEndTime = 0
timerActive = False
if __name__ == "__main__":
    queue = Queue()

    _context = None
    while True:
        queue.put(message)
        chatBotThread = Thread(target=chatBot, args=(queue,))
        waitingThread = Thread(target=passTime)
        exCam = Thread(target=exerciseCamera())

        chatBotThread.daemon = True
        chatBotThread.start()
        waitingThread.start()
        exCam.start()

        # print(chatBotThread.is_alive())
        chatBotThread.join()
        # waitingForInput = False
        message = queue.get()

        print(message)
        bestFit, context = analyzeResponse(message["Message"], _context)
        _context = context

        print(bestFit)
        # re = queue.get()
        # print(re)
        # print(chatBotThread.is_alive())

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

#
# KEY = "Server"
# HEADER = 160
# HOSTNAME = gbhn(ghn())
# PORT_NUMBER = 54124
# SERVER_ADDRESS_PORT = (HOSTNAME, PORT_NUMBER)
# FORMAT = "utf-8"
# DISCONNECTING_MESSAGE = "Disconnecting"
# server = socket(AF_INET, SOCK_STREAM)
# server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# server.bind(SERVER_ADDRESS_PORT)
#
#
# def ReceiveClientMessage(connection): #, queue_: Queue):
#     connected = True
#     while connected:
#         try:
#             msgLength = connection.recv(HEADER).decode(FORMAT)
#             if msgLength:
#                 msgLength = int(msgLength)
#                 msg = connection.recv(msgLength).decode(FORMAT)
#                 # queue_.put(msg)
#
#                 if DISCONNECTING_MESSAGE in msg:
#                     print(msg)
#                     # try:
#                     #     clients.remove(msg)
#                     #     print(msg, "Removed\n")
#                     # except ValueError:
#                     #     pass
#                     # connected = False
#                     # connection.close()
#                 else:
#                     msg = msg.strip()
#                     msg = msg.lower()
#                     msg = checkClientMessage(msg)
#                     if "timer done" == msg:
#                         print("Timer Done")
#                     if msg is not None:
#                         print(msg, "\n")
#
#         except ConnectionResetError:
#             print("reset")
#             pass
#
#
# def checkClientMessage(msg: str):
#     if "starting timer for" in msg.lower():
#         global currentTimerTime
#         global timerActive
#         global queue
#         # queue = Queue()
#         # queue.put(currentTimerTime)
#
#         amountOfTime = [int(num) for num in msg.split() if num.isdigit()][0]
#
#         if "seconds" in msg:
#             # startTimer = Process(target=timer, args=([0, 0, amountOfTime], queue))
#             startTimer([0, 0, amountOfTime])
#         #     unit = "seconds"
#         # elif "minutes" in msg:
#         #     startTimer = Process(target=timer, args=([0, amountOfTime, 0], queue))
#         #     unit = "minutes"
#         # elif "hours" in msg:
#         #     startTimer = Process(target=timer, args=([amountOfTime, 0, 0], queue))
#         #     unit = "hours"
#
#         # startTimer.start()
#         timerActive = True
#         # startTimer.join()
#
#     elif "pausing timer" in msg.lower():
#         # put the timer function in the main file if else
#
#         # If user tries to pause the timer, the
#         try:
#             # startTimer.terminate()
#             timerActive = False
#             # pausedTimerTime = timerEndTime - int(t())
#             timeLeft = checkTimer()
#             print("Timer Paused At:", timeLeft)
#         except AttributeError:
#             pass
#
#     else:
#         return msg
#
#     return None
#
#
# def sendClientMessage(connection, msg: str, toClient):
#     msg = msg.encode(FORMAT)
#     msgLength = len(msg)
#     sendLength = str(msgLength).encode(FORMAT)
#     sendLength += b" " * (HEADER - len(sendLength))
#     # try:
#     #     connection.send(msg)
#     # except ConnectionResetError:
#     #     try:
#     #         # clients.remove(toClient)
#     #     except ValueError:
#     #         pass
#
#
# def startTimer(timerFor):
#     global startingTimer
#     global timerEndTime
#     timeToAdd = (timerFor[0] * 3600) + \
#                 (timerFor[1] * 60) + \
#                 (timerFor[2])
#
#     startingTimer = int(t())
#     timerEndTime = startingTimer + timeToAdd
#
#
# def startServer():
#     server.listen()
#     print(f"Listening ON {HOSTNAME}\n")
#     global queue
#     global msg_
#     global timerEndTime
#
#     # queue = Queue()
#     # queue.put(msg_)
#     while True:
#         print("here")
#         connection, address = server.accept()
#         serverListen = Thread(target=ReceiveClientMessage, args=(connection,))
#         serverListen.start()
#         # serverListen.join()
#         # print(checkTimer(queue))
#         # print(queue.get())
#         # print(checkTimer(), timerEndTime)
#         s(.25)
#
#
# # keep a variable with the information of the world time + the timer, then check each loop
#
# # msg_ = ""
# # queue = Queue()
# # currentTimerTime = {"Timer:": None}
# # startingTimer = None
# #
# # print("Starting Server")
# # clients = []
# # speakingTo = []
#
#


# # def checkTimer(info=None):
# #     global timerEndTime
# #     if info is None:
# #         timeLeft = timerEndTime - int(t())
# #         if timeLeft <= 0:
# #             return "Timer Done"
# #         else:
# #             return timeLeft





# from speechMain import chatBot
# def chatBot(msg: Queue = None):
#     userInput = input("Type your Message:\n>>>")
#     # if msg is None:
#     #     return
#     _msg = msg.get()
#     _msg["Message"] = userInput
#     msg.put(_msg)
#     return
#
#
#
#
# from speechFunct import analyzeResponse
# message = {"Message": ""}
# if __name__ == "__main__":
#     # startServer()
#     queue = Queue()
#
#     _context = None
#     while True:
#         queue.put(message)
#         chatBotThread = Thread(target=chatBot, args=(queue,))
#
#         chatBotThread.daemon = True
#         chatBotThread.start()
#         # print(chatBotThread.is_alive())
#         chatBotThread.join()
#
#         message = queue.get()
#
#         print(message)
#         bestFit, context = analyzeResponse(message["Message"], _context)
#         _context = context
#
#         print(bestFit)
#         # re = queue.get()
#         # print(re)
#         # print(chatBotThread.is_alive())

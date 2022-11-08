import sys
from time import time as t, sleep as s
from client import ClientMessaging
# from threading import Thread
from multiprocessing import Manager, Process


def timer(timerFor, queue=None):
    startTime = int(t())
    totalTime = (timerFor[0] * 3600) + \
                (timerFor[1] * 60) + \
                (timerFor[2])

    oldElapsed = None
    while True:
        currentTime = int(t())
        elapsed = currentTime - startTime

        timeLeft = totalTime - elapsed
        # if queue is not None:
            # try:
        currentTimerTime = queue.get()
        currentTimerTime["Timer"] = timeLeft
        queue.put(currentTimerTime)
        ClientMessaging.sendServerMessage(timeLeft)
            # except BrokenPipeError:
            #     pass

        if elapsed > totalTime:
            print("\rTimer Done")
            print()
            ClientMessaging.sendServerMessage("Timer Done")
            return True

        else:
            if oldElapsed != elapsed:
                oldElapsed = elapsed
                # Show Timer Countdown
                sys.stdout.write(f"\rTime Left: {timeLeft}")
                sys.stdout.flush()


#
# def waitAndListen():
#     while True:
#         print("Waiting And Listening")
#         try:
#             msg = ClientMessaging.receiveServerMessage()
#             if "Timer Function" in msg:
#                 if "Resume Timer":
#                     return
#         except ConnectionError:
#             pass
#
#         s(1)


# Hours, Minutes, Seconds
# timed = [0, 0, 1]
# timer(timed)
# ___________________________________________




# def worker1(time, return_dict1):
#     newTime = 0
#     global running
#
#     while running:
#         s(1)
#         newTime += 1
#         try:
#             new = time - newTime
#             print("out:", new)
#             return_dict1[time] = new
#         except BrokenPipeError:
#             pass
#
#
# def inpuT():
#     for x in range(4):
#         print("in:", x)
#         s(1)
#     return
#
#
# running = True
# if __name__ == "__main__":
#     manager = Manager()
#     return_dict1 = manager.dict()
#
#     p1 = Process(target=worker1, args=(5, return_dict1))
#     p1.start()
#     p2 = Process(target=inpuT)
#     p2.start()
#
#
#     # p.join()
#     # p1.join()
#     p2.join()
#
#     running = False
#     p1.terminate()
#     # p.terminate()
#
#     print("Here", return_dict1.values())




# ___________________________________________
# from threading import Thread
# import time
#
# thread_running = True
#
#
# def my_forever_while():
#     global thread_running
#
#     start_time = time.time()
#
#     # run this while there is no input
#     while thread_running:
#         time.sleep(0.1)
#
#         if time.time() - start_time >= 5:
#             start_time = time.time()
#             print('Another 5 seconds has passed')
#
#
# def take_input():
#     user_input = input('Type user input: ')
#     # doing something with the input
#     print('The user input is: ', user_input)
#
#
# if __name__ == '__main__':
#     t1 = Thread(target=my_forever_while)
#     t2 = Thread(target=take_input)
#
#     t1.start()
#     t2.start()
#
#     t2.join()  # interpreter will wait until your process get completed or terminated
#     thread_running = False
#     print('The end')

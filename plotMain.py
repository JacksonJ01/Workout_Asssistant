# from numpy import *
from plotFunct import plotPoint, plotLine
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation as fan
import keyboard
from random import randint, shuffle
from time import sleep as s, time


def pointed():
    point0 = [0, 6, 5]  # Nose
    point1 = [.5, 6.25, 5]  # EyeIn
    point2 = [.7, 6.25, 5]  # Left Eye
    point3 = [.9, 6.25, 5]  # EyeOut
    point4 = [-.5, 6.25, 5]  # EyeIn
    point5 = [-.7, 6.25, 5]  # Right Eye
    point6 = [-.9, 6.25, 5]  # EyeOut
    point7 = [1.4, 6, 5]  # Left Ear
    point8 = [-1.4, 6, 5]  # Right Ear
    point9 = [.5, 5.75, 5]  # Left Mouth
    point10 = [-.5, 5.75, 5]  # Right Mouth
    point11 = [2, 5, 5]  # Left Shoulder
    point12 = [-2, 5, 5]  # Right Shoulder
    point13 = [2.75, 4, 5]  # Left Elbow
    point14 = [-2.75, 4, 5]  # Right Elbow
    point15 = [3.5, 4.7, 5]  # Left Wrist
    point16 = [-3.5, 4.7, 5]  # Right Wrist
    point17 = [4, 4.7, 5]  # Left Pinky
    point18 = [-4, 4.7, 5]  # Right Pinky
    point19 = [3.75, 4.9, 5]  # Left Index
    point20 = [-3.75, 4.9, 5]  # Right Index
    point21 = [3.5, 4.8, 5]  # Left Thumb
    point22 = [-3.5, 4.8, 5]  # Right Thumb
    point23 = [1.5, 3, 5]  # Left Hip
    point24 = [-1.5, 3, 5]  # Right Hip
    point25 = [2, 2, 5]  # Left Knee
    point26 = [-2, 2, 5]  # Right Knee
    point27 = [1.5, 1, 5]  # Left Ankle
    point28 = [-1.5, 1, 5]  # Right Ankle
    point29 = [1.25, .5, 5]  # Left Heel
    point30 = [-1.25, .5, 5]  # Right Heel
    point31 = [2.85, .5, 5]  # Left Foot Index
    point32 = [-2.85, .5, 5]  # Right Foot Index

    points = [point0,
              point1, point2, point3,
              point4, point5, point6,
              point7, point8,
              point9, point10,
              point11, point12,
              point13, point14,
              point15, point16,
              point17, point18,
              point19, point20,
              point21, point22,
              point23, point24,
              point25, point26,
              point27, point28,
              point29, point30,
              point31, point32]

    return points


def plot(points=None):
    fig = plt.figure(figsize=(5, 5))

# timeStamp = time()
    while True:
        # if time() - timeStamp >= .5:
        #     print("Here")
        #     plt.clf()
        #     timeStamp = time()
        #
        #     axis = fig.add_subplot(111, projection="3d")
        #     axis.set_title("3D Space")
        #     # plt.ion()
        #     plt.xlabel("X Axis")
        #     plt.ylabel("Y Axis")

        axis = fig.add_subplot(111, projection="3d")
        axis.set_title("3D Space")
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plt.ion()

        if points is None:
            points = pointed()

        # current = None
        _next = None

        for num, x in enumerate(points):
            current = x
            try:
                _next = points[num + 1]
            except IndexError:
                plotPoint(current, axis)

            if num in [0, 7, 8, 21, 22]:
                plotPoint(x, axis)

            if num in [11, 12]:
                _next = points[num + 12]
                plotLine(current, _next, axis)

            if num in [15, 16,
                       27, 28]:
                _next = points[num + 2]
                _next2 = points[num + 4]

                plotLine(current, _next, axis)
                plotLine(_next, _next2, axis)
                plotLine(_next2, current, axis)

            if num in [11, 12,
                       23, 24]:

                _next = points[num + 2]
                _next2 = points[num + 4]

                plotLine(current, _next, axis)
                plotLine(_next, _next2, axis)

            if num in [1, 2, 4, 5, 9, 11, 23]:
                _next = points[num + 1]
                plotLine(current, _next, axis)  # , num, num, num, num)

        plt.draw()
        plt.pause(1)
        # plt.clf()

        # plt.show()
        # while True:
        try:
            if keyboard.is_pressed("q"):
                plt.close()
                quit()
        except ValueError:
            pass
            # break


    # return plt


# plot()

from tkinter import Entry, Label, Tk, StringVar
from PIL import ImageTk, Image
from cv2 import cvtColor, COLOR_BGR2RGB, VideoCapture
from cameraFunct import *
from speechFunct import analyzeResponse

from threading import Thread


# Interface for the chatBot functions #

Context = None
Response = "Response"

def chatWithChatBot(event):
    global Context
    global Response
    _msg = inputField.get()
    Response, Context = analyzeResponse(_msg, Context)
    print("Response:", Response)
    inputField.delete(0, 'end')


# Interface for the cameraMain video feed #
#
def closeFull(event):
    window.attributes("-fullscreen", False)


def openFull(event):
    window.attributes('-fullscreen', True)


def closeWindow(event):
    window.quit()


window = Tk()
window.bind("<Left>", closeFull)
window.bind("<Right>", openFull)
window.bind("<Escape>", closeWindow)
window.title("Camera feed")
window.geometry("700x350")

# Create a Label to capture the Video frames
label = Label(window)
label.grid(row=1, column=0, rowspan=2)

# VidCapture = VideoCapture(0)
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test1.gif")
VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test3.gif")
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test4.gif")
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test5.gif")
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test6.gif")
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test7.gif")
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test8.gif")
# VidCapture = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test9.gif")
# _____________________________________
mPose = mp.solutions.pose
Pose_ = mPose.Pose()
DrawLM = mp.solutions.drawing_utils

pTime = 0

# Thinking of tracking the positioning of
# tracked = {"nose": [],
#            "leftShoulder|leftWrist": [], "rightShoulder|rightWrist": [],
#            "leftHip|LeftAnkle": [], "rightHip|rightAnkle": []}

ExerciseDict = {}

VerificationTime = .1  # The program will take 2x seconds to verify the workout
StartingPreparations = time()
BeginVerification = None

Assumption = None
AssumptionMade = False
Known = False
ConfirmedExercise = ""  # "bicep curl"

ExercisesCompletedList = []
ExerciseCount = 0
NOrLatch = False
RepCount = 0

endWorkout = False

endTime = None

xLength = 720
yHeight = 480
VidCapture.set(3, xLength)
VidCapture.set(4, yHeight)

#
ExName = Exercise

DownTime = 5
CurrentDownTime = time()
# firstTimeCheckBool = True
MinimumRepCount = 1

_input = StringVar()
inputField = Entry(window, textvariable=_input, width=80, bg="white", fg="black", borderwidth=5, )
inputField.bind("<Return>", chatWithChatBot)
inputField.grid(row=4, column=0)

responseLabel = Label(window, width=70, bg="black", fg="white", borderwidth=0)
curExLabel = Label(window, text="Current Exercise", width=43, height=10, font=("Arial", 13), bg="black", fg="white", borderwidth=0)
paddedLabel = Label(window, text="Target Range", anchor="w", width=48, height=12, font=("Arial", 12), bg="black", fg="white", borderwidth=0)

responseLabel.grid(row=3, column=0)
curExLabel.grid(row=1, column=1)
paddedLabel.grid(row=2, column=1)

RepCompleted = [False, None]
Assumption2 = None


# Define function to show frame

def cv2VideoFrames():
    try:
        # Get the latest frame and convert into Image
        # image = cvtColor(VidCapture.read()[1], COLOR_BGR2RGB)
        image = imageProcessing()
        image = cvtColor(image, COLOR_BGR2RGB)
        padded = RepCompleted[1]
        # print(padded)
        img = Image.fromarray(image)
        # Convert image to PhotoImage
        imgtk = ImageTk.PhotoImage(image=img)

        label.imgtk = imgtk
        label.configure(image=imgtk)
    except error:
        pass
        # quit(0)

    try:

        responseLabel.configure(text=Response)

        curExLabel.configure(text=(ConfirmedExercise + "\nRep Count: " + str(RepCount) + "\nExerDict: " + str(ExerciseDict)))
        paddedLabel.configure(text=(str(RepCompleted[1]) + "\n\nIn Target Range: " + str(RepCompleted[0])))
        # Repeat after an interval to capture continuously
        label.after(20, cv2VideoFrames)

        # print("\nWithin Repetition Target Range:", RepCompleted[0])
        # print(ExerciseDict)
        # print("Repetition Tracker:", RepCount)

    except error:
        pass
        # quit(0)


def imageProcessing():
    global VidCapture
    global Pose_
    global DrawLM
    global ExName
    global Known
    global ConfirmedExercise
    global pTime
    global NOrLatch
    global RepCount
    global Assumption
    global Assumption2
    global AssumptionMade
    global CurrentDownTime
    global DownTime
    global StartingPreparations
    global BeginVerification
    global RepCompleted

    img = None
    try:
        img, Assumption2, ExName, \
        RepCompleted, trackedAngles, \
        allLocations = readImg(VidCapture, Pose_, DrawLM, ExName,
                               showInterest=True, showDots=False,
                               showLines=True, showText=True, known=Known,
                               confirmedExercise=ConfirmedExercise)
        # print(allLocations)
        convertedLoc = []
        # Loop to adjust the Y cords of the location
        for cor in allLocations:
            new = cor[1], yHeight - cor[2], cor[3]
            convertedLoc.append(new)

        # server.sendto(str.encode(str(convertedLoc)), serverAddressPort)
        # print(convertedLoc)

    except TypeError:
        pass

    pTime = fps(img, pTime)
    elapsedTime = time()

    if Known is True:
        # if firstTimeCheckBool is True:
        #     firstTimeCheckBool = False
        # currentDownTime = time()

        # Here 09/17/22

        if RepCompleted[0] is True and NOrLatch is False:
            RepCount += 1
            NOrLatch = True
            CurrentDownTime = int(time())

        elif RepCompleted[0] is False and NOrLatch is True:
            NOrLatch = False

        if RepCompleted[0] is False:
            if int(time()) - CurrentDownTime >= DownTime:
                Known = False
                AssumptionMade = False
                StartingPreparations, CurrentDownTime = time(), time()

                if ExName.mirrored is False:
                    RepCount /= 2

                if RepCount > MinimumRepCount:
                    if ConfirmedExercise not in ExerciseDict:
                        ExerciseDict[ConfirmedExercise] = RepCount
                    else:
                        ExerciseDict[str(ConfirmedExercise) + "*"] = RepCount
                    RepCount = 0

                # reset the values
        # print(ExerciseDict)
        # print("Repetition Tracker:", RepCount)

    else:
        # This allows the program to get an initial idea on what the exercise might be
        # Once it makes this assumption, the computer will wait x amount of time before checking again
        if (elapsedTime - StartingPreparations) > VerificationTime and AssumptionMade is False:

            try:
                if AssumptionMade is False:
                    Assumption = Assumption2
                    # print("First assumption:", Assumption)
                    AssumptionMade = True
                    BeginVerification = time()
            except IndexError or TypeError:
                AssumptionMade = False

            # Once x amount of time passes, the computer will make it's second check
            # If current assumption matches the prior assumption, then the exercise will be seen as known

        if AssumptionMade is True:
            if (elapsedTime - BeginVerification) > VerificationTime:
                # print("\nTime Elapsed:", float(elapsedTime - BeginVerification))
                # print("assumption1:", Assumption, " | assumption2:", Assumption2)
                try:
                    if Assumption == Assumption2 and Assumption2 is not None:
                        ConfirmedExercise = Assumption
                        # print("\nExercise Confirmed:", ConfirmedExercise, "\n")
                        Known = True

                except IndexError or TypeError:
                    AssumptionMade = False

                # If the assumed workout doesn't match, then the process will start over
                else:
                    Assumption = Assumption2
                    StartingPreparations = time()
                    AssumptionMade = False

    try:
        # imshow("Picture", img)
        return img
    except error:
        pass

    if waitKey(1) & 0xFF == ord('q'):
        if RepCount > MinimumRepCount:
            if ConfirmedExercise not in ExerciseDict:
                ExerciseDict[ConfirmedExercise] = RepCount
            else:
                ExerciseDict[str(ConfirmedExercise) + "*"] = RepCount
            RepCount = 0

        print(ExerciseDict)

        terminateWindows(VidCapture)
        quit()

    return img


cv2VideoFrames()
window.mainloop()

# print("here")

# Interface for the placement display #


# _________________________
# Messing Around
# class Staff:
#     def __init__(self, name: str, days: list):
#         self.staffName = name
#         self.daysAvailable = days
#
#
# def evaluateInfo(people: list):
#
#     days = {0: [],  # Sunday
#             1: [], 2: [], 3: [], 4: [], 5: [],  # Weekdays
#             6: []}  # Saturday
#
#     numDaysAvailable = {
#         1: [], 2: [], 3: [],
#         4: [], 5: [], 6: [],

#         0: []
#     }
#
#     for peep in people:
#         num = peep.daysAvailable.count(1)
#
#         try:
#             numDaysAvailable[num].append(peep.staffName)
#         except KeyError as e:
#             print(e)
#
#         for day in days.keys():
#             if peep.daysAvailable[day] == 1:
#                 days[day].append(peep.staffName)
#
#     return numDaysAvailable, days
#
#
# def createSchedule(people: list, daysToSchedule: list):
#
#     numDaysAvailable, days = evaluateInfo(people)
#     schedule = []
#     countDays = daysToSchedule.count(1)
#     numPeople = len(people)
#
#     print(days, " |\n ", numDaysAvailable)
#     # print(numPeople % countDays)
#
#     if numPeople <= countDays:
#         while True:
#             pass
#         pass
#
#     elif countDays < numPeople:
#         while True:
#             pass
#         pass
#
#
# Jared = Staff("Jared", [-1, 0, 0, 0, 0, 1, 1])
# Nicole = Staff("Nicole", [1, -1, 1, 1, -1, -1, 0])
# Gianny = Staff("Gianny", [-1, 1, 0, 1, -1, 0, 0])
# Jonathan = Staff("Jonathan", [0, 1, 0, 1, 1, -1, -1])
# Zachary = Staff("Zachary", [0, 1, 1, 1, 0, 0, -1])
# Alana = Staff("Alana", [1, 1, 0, 1, -1, -1, -1])
# Clara = Staff("Clara", [0, 1, -1, 1, 1, -1, -1])
# Lauren = Staff("Lauren", [0, 0, 0, 0, 0, 1, 1])
# Jules = Staff("Jules", [0, -1, 1, 1, -1, 0, 0])
# Chesachi = Staff("Chesachi", [1, 1, 1, 0, 0, -1, -1])
#
#
# staffMembers = [Jared, Nicole, Gianny, Jonathan,
#                 Zachary, Alana, Clara,
#                 Lauren, Jules, Chesachi]
# Week = [0, 0, 0, 0, 0, 1, 1]
#
# createSchedule(staffMembers, Week)

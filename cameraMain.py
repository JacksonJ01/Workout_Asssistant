from cv2 import cvtColor, COLOR_BGR2RGB, VideoCapture, waitKey
from cameraFunct import *

# from plotMain import plot
from PIL import Image
from socket import socket, AF_INET, SOCK_DGRAM


# _____________________________________________________________________________
def exerciseCamera(defaultCam=1):
    mPose = mp.solutions.pose
    pose = mPose.Pose()
    drawLM = mp.solutions.drawing_utils

    pTime = 0

    # Thinking of tracking the positioning of
    # tracked = {"nose": [],
    #            "leftShoulder|leftWrist": [], "rightShoulder|rightWrist": [],
    #            "leftHip|LeftAnkle": [], "rightHip|rightAnkle": []}

    exerciseDict = {}
    verificationTime = .1  # The program will take 2x seconds to verify the workout
    startingPreparations = time()
    beginVerification = None

    assumption = None
    assumptionMade = False
    known = False
    confirmedExercise = ""  # "bicep curl"

    video = None
    exercisesCompletedList = []
    exerciseCount = 0
    nOrLatch = False
    repCount = 0

    endWorkout = False
    # If the user hasn't started a new postion after x amount of time, stop the workout
    if defaultCam == 0:
        video = VideoCapture(0)
    elif defaultCam == (0, 1):
        print("Okay")
        video = VideoCapture(1)
    elif defaultCam == 1:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test1.gif")  # Single Arm Bicep Curl
    elif defaultCam == 2:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test2.mp4")  # Bicep Curl 2
    elif defaultCam == 3:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test3.gif")  # Bicep Curls  need new
    elif defaultCam == 4:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test4.gif")  # Squat
    elif defaultCam == 5:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test5.gif")  # Back Squat 2
    elif defaultCam == 6:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test6.gif")  # Squat 3  need new
    elif defaultCam == 7:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test7.gif")  # Front Squats
    elif defaultCam == 8:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test8.gif")  # Front Squats
    elif defaultCam == 9:
        video = VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test9.gif")

    endTime = None
    if defaultCam == 1 or 2 < defaultCam:
        gif = Image.open("C:\\Users\\Big Boi J\\Downloads\\test{}.gif".format(defaultCam))
        lengthOfGif = findDur(gif)
        startTime = int(time())
        endTime = int(startTime + (lengthOfGif / 2))

    xLength = 720
    yHeight = 480
    video.set(3, xLength)
    video.set(4, yHeight)

    #
    # Communication
    # server = socket(AF_INET, SOCK_DGRAM)
    # serverAddressPort = ("127.0.0.1", 54124)
    exName = None

    downTime = 5
    currentDownTime = time()
    #firstTimeCheckBool = True
    minimumRepCount = 1
    while True:
        # print(int(time()), endTime)
        # if endTime is not None and endTime <= time():
        #     cv2.destroyAllWindows()
        #     # print("Closed 1")
        #     break

        try:
            img, assumption2, exName, \
            repCompleted, trackedAngles, \
            allLocations = readImg(video, pose, drawLM, exName,
                                   showInterest=True, showDots=False,
                                   showLines=True, showText=True, known=known,
                                   confirmedExercise=confirmedExercise)
            # print(allLocations)
            convertedLoc = []
            # Loop to adjust the Y cords of the location
            for cor in allLocations:
                new = cor[1], yHeight - cor[2], cor[3]
                convertedLoc.append(new)

            # server.sendto(str.encode(str(convertedLoc)), serverAddressPort)
            # print(convertedLoc)

        except TypeError:
            continue

        pTime = fps(img, pTime)
        elapsedTime = time()

        if known is True:
            # if firstTimeCheckBool is True:
            #     firstTimeCheckBool = False
                # currentDownTime = time()

            # Here 09/17/22
            print("\nWithin Repetition Target Range:", repCompleted)
            if repCompleted is True and nOrLatch is False:
                repCount += 1
                nOrLatch = True
                currentDownTime = int(time())

            elif repCompleted is False and nOrLatch is True:
                nOrLatch = False

            if repCompleted is False:
                if int(time()) - currentDownTime >= downTime:
                    known = False
                    assumptionMade = False
                    startingPreparations, currentDownTime = time(), time()

                    if exName.mirrored is False:
                        repCount /= 2

                    if repCount > minimumRepCount:
                        if confirmedExercise not in exerciseDict:
                            exerciseDict[confirmedExercise] = repCount
                        else:
                            exerciseDict[str(confirmedExercise) + "*"] = repCount
                        repCount = 0

                    # reset the values
            print(exerciseDict)
            print("Repetition Tracker:", repCount)

        else:
            # This allows the program to get an initial idea on what the exercise might be
            # Once it makes this assumption, the computer will wait x amount of time before checking again
            if (elapsedTime - startingPreparations) > verificationTime and assumptionMade is False:

                try:
                    if assumptionMade is False:
                        assumption = assumption2
                        print("First assumption:", assumption)
                        assumptionMade = True
                        beginVerification = time()
                except IndexError or TypeError:
                    assumptionMade = False

                # Once x amount of time passes, the computer will make it's second check
                # If current assumption matches the prior assumption, then the exercise will be seen as known

            if assumptionMade is True:
                if (elapsedTime - beginVerification) > verificationTime:
                    print("\nTime Elapsed:", float(elapsedTime - beginVerification))
                    print("assumption1:", assumption, " | assumption2:", assumption2)
                    try:
                        if assumption == assumption2 and assumption2 is not None:
                            confirmedExercise = assumption
                            print("\nExercise Confirmed:", confirmedExercise, "\n")
                            known = True

                    except IndexError or TypeError:
                        assumptionMade = False

                    # If the assumed workout doesn't match, then the process will start over
                    else:
                        assumption = assumption2
                        startingPreparations = time()
                        assumptionMade = False

        try:
            imshow("Picture", img)
            pass
        except error:
            pass

        if waitKey(1) & 0xFF == ord('q'):
            if repCount > minimumRepCount:
                if confirmedExercise not in exerciseDict:
                    exerciseDict[confirmedExercise] = repCount
                else:
                    exerciseDict[str(confirmedExercise) + "*"] = repCount
                repCount = 0

            print(exerciseDict)
            quit()

    terminateWindows(video)


# _______________________________________________________________________________________________
# exerciseCamera(0)
# exerciseCamera((0, 1))
# exerciseCamera(1)   # Single Arm Bicep Curls | 3 reps
# exerciseCamera(2)   # Bicep Curls | 5 reps
# exerciseCamera(3)   # Bicep Curls | 5 reps
# exercise3Camera(4)  # Needs Replacement | Record Single Arm Bicep Curls on the Computer From Different Camera Angles
# exerciseCamera(5)   # Needs Replacement | Currently Buggy Squats | Record Bicep Curls on the Computer From Different Camera Angle

# exerciseCamera(6)   # Goblet Squats
# exerciseCamera(7)   # Goblet Squats
# exerciseCamera(8)   # Barbell Squats
# exerciseCamera(9)   # Need Barbell Squats | Record Barbell Squats on the Computer From Different Angles
# exerciseCamera(10)  #

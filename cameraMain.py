from cameraFunct import *
from plotMain import plot
from socket import socket, AF_INET,\
    SOCK_DGRAM, SOCK_STREAM, gethostname as ghn, gethostbyname as gbhn


# _____________________________________________________________________________
def exerciseCamera(defaultCam=1):
    mPose = mp.solutions.pose
    pose = mPose.Pose()
    drawLM = mp.solutions.drawing_utils

    pTime = 0

    # Thinking of tracking the positioning of
    tracked = {"nose": [],
               "leftShoulder|leftWrist": [], "rightShoulder|rightWrist": [],
               "leftHip|LeftAnkle": [], "rightHip|rightAnkle": []}

    verificationTime = .2  # The program will take 2x seconds to verify the workout
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

    started = False

    if defaultCam == 0:
        video = cv2.VideoCapture(0)
    elif defaultCam == 1:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test1.gif")  # Bicep Curl
    elif defaultCam == 2:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test2.gif")  # Bicep Curl 2
    elif defaultCam == 3:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test6.gif")  # Bicep Curls  need new
    elif defaultCam == 4:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test3.gif")  # Squat
    elif defaultCam == 5:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test4.gif")  # Back Squat 2
    elif defaultCam == 6:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test5.gif")  # Squat 3  need new
    elif defaultCam == 7:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test7.gif")  # Front Squats
    elif defaultCam == 8:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test8.gif")  # Front Squats
    elif defaultCam == 9:
        video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test9.gif")

    xLength = 1080
    yHeight = 720
    video.set(3, xLength)
    video.set(4, yHeight)

    #
    # Communication
    server = socket(AF_INET, SOCK_DGRAM)
    serverAddressPort = ("127.0.0.1", 54124)

    while True:
        try:
            img, assumption2, repCompleted, allLocations = readImg(video, pose, drawLM, showInterest=True,
                                                                   showDots=False, showLines=True,
                                                                   showText=True, known=known,
                                                                   confirmedExercise=confirmedExercise)




            # print(allLocations)
            convertedLoc = []
            # Loop to adjust the Y cords of the location
            for cor in allLocations:
                new = cor[1], yHeight - cor[2], cor[3]
                convertedLoc.append(new)

            server.sendto(str.encode(str(convertedLoc)), serverAddressPort)
            print(convertedLoc)

        except TypeError:
            continue

        pTime = fps(img, pTime)
        elapsedTime = time()

        if known is True:
         # Here 09/17/22
            print("repCompleted:", repCompleted)
            if repCompleted is True and nOrLatch is False:
                repCount += 1
                nOrLatch = True

            elif repCompleted is False and nOrLatch is True:
                nOrLatch = False

            print("repCount:", repCount)

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
                    print("Time to evaluate", elapsedTime - beginVerification)
                    print("assumption1:", assumption, " | assumption2:", assumption2)
                    try:
                        if assumption == assumption2 and assumption2 is not None:
                            confirmedExercise = assumption
                            print("Exercise Confirmed:", confirmedExercise)
                            known = True

                    except IndexError or TypeError:
                        assumptionMade = False

                    # If the assumed workout doesn't match, then the process will start over
                    else:
                        assumption = assumption2
                        startingPreparations = time()
                        assumptionMade = False

        try:
            cv2.imshow("Image", img)
        except cv2.error:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            quit()

    terminateWindows(video)


# _____________________________________________________________________________
def gameCamera(defaultCam=1, video=None):
    ipAddress = "127.0.0.1"
    portNumber = 54124
    server = socket(AF_INET, SOCK_DGRAM)
    serverAddressPort = (ipAddress, portNumber)

    mPose = mp.solutions.pose
    pose = mPose.Pose()
    drawLM = mp.solutions.drawing_utils

    xLength = 1080
    yHeight = 720

    # I am just realizing these gifs only work on my laptop
    if defaultCam == 0:
        video = cv2.VideoCapture(0)
    else:
        exit("Wrong Fucntion")

    video.set(3, xLength)
    video.set(4, yHeight)

    while True:
        try:
            img, _, _, allLocations = readImg(video, pose, drawLM, showInterest=True, showDots=False, showLines=True,
                                              showText=True)

            print(allLocations)
            convertedLoc = []
            # Loop to adjust the Y cords of the location
            for cor in allLocations:
                new = cor[1], yHeight - cor[2], cor[3]
                convertedLoc.append(new)

            # print(convertedLoc)

            try:
                cv2.imshow("Image", img)
            except cv2.error:
                pass

            if cv2.waitKey(1) & 0xFF == ord('z'):
                terminateWindows(video)
                quit()

            server.sendto(str.encode(str(convertedLoc)), serverAddressPort)

        except TypeError:
            pass


# _____________________________________________________________________________
def cameraPlotting():
    mPose = mp.solutions.pose
    pose = mPose.Pose()
    drawLM = mp.solutions.drawing_utils
    # img = None
    video = cv2.VideoCapture(0)
    # video = cv2.VideoCapture("C:\\Users\\Big Boi J\\Downloads\\test6.gif")
    while True:
        try:
            img, _, _, allLocations = readImg(video, pose, drawLM, showInterest=True, showDots=False, showLines=True,
                                              showText=True)

            # print(allLocations)
            cv2.imshow("Image", img)

            try:
                plotCords = []
                for x in allLocations:
                    plotting = [x[1], x[2], x[3]]
                    plotCords.append(plotting)

                print(plotCords)
                plot(plotCords)

            except TypeError:
                pass

        except cv2.error or TypeError:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    terminateWindows(video)
    return


#_______________________________________________________________________________________________
# gameCamera()
exerciseCamera(1)
# 1, 2, , 4, 5, , ,7 ,8 ,9
# cameraPlotting()

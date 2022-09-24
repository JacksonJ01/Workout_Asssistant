import cv2
import mediapipe as mp
from math import atan2, pi
from time import time  # , sleep as s


def readImg(video, pose, drawLM, showInterest=False, showDots=False,
            showLines=False, showText=True, known=False, confirmedExercise=None):
    _, img = video.read()
    try:
        img = cv2.resize(img, (1080, 720))
    except cv2.error:
        pass
    if not _:
        return

    img, results = findLandmarks(img, pose)
    img, locationsOfInterest, allLocations = getLandmarkLocations(img, drawLM, results, showInterest, showDots,
                                                                  showLines)
    assumption = None
    try:
        img, leftAngles, rightAngles = calculateAngle(img, locationsOfInterest, showText)
        if known is True:
            return img, assumption, detectRepetitions(confirmedExercise, leftAngles, rightAngles), allLocations
        else:
            assumption = detectExercise(leftAngles, rightAngles, allLocations)

    except TypeError:
        pass

    # print('\n', locationsOfInterest)
    # print(leftAngles)
    # print(rightAngles)

    return img, assumption, False, allLocations


# _____________________________________________________________________________
def findLandmarks(img, pose):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB).pose_landmarks
    # displayText(img, "", "")
    return img, results


# _____________________________________________________________________________
def getLandmarkLocations(img, drawLM, results, showInterest=False, showDots=False, showLines=False):
    locationsOfInterests = []
    allLocations = []
    if results:
        if showLines is True:
            connDots = mp.solutions.pose.POSE_CONNECTIONS
            drawLM.draw_landmarks(img, results, connDots)

        elif showDots is True:
            drawLM.draw_landmarks(img, results)

        for num, info in enumerate(results.landmark):
            # print(num, "vis", coord.visibility)
            # Nose 0,
            # leftShoulder 11, leftElbow 13, leftWrist 15,
            # rightShoulder 12, rightElbow 14, rightWrist 16,
            # leftHip 23, leftKnee 25, leftAnkle 27,
            # rightHip 24, rightKnee 26, rightAnkle 28

            # print(info)
            h, w, c = img.shape
            xcor, ycor, zcor, vis = int(info.x * w), int(info.y * h), info.z, info.visibility
            allLocations.append((num, xcor, ycor, zcor, vis))

            if num in [0, 11, 12, 13, 14, 15, 16,
                       23, 24, 25, 26, 27, 28]:
                locationsOfInterests.append((num, xcor, ycor, vis))

                if showDots is True or showInterest is True:
                    cv2.circle(img, (xcor, ycor), 5, (0, 0, 0), cv2.FILLED)

    # print(locationsOfInterests)
    return img, locationsOfInterests, allLocations


# _____________________________________________________________________________
def calculateAngle(img, locationsOfInterest, showText=False):
    # displayText(img, "", "")
    leftAngles = []
    rightAngles = []
    for sub, points in enumerate(locationsOfInterest):
        try:
            x1, y1 = None, None
            x2, y2 = None, None
            x3, y3 = None, None

            if sub in [1, 2, 7, 8]:
                _, x1, y1, _ = locationsOfInterest[sub]
                _, x2, y2, _ = locationsOfInterest[sub + 2]
                _, x3, y3, _ = locationsOfInterest[sub + 4]

            elif sub in [3, 4]:
                _, x1, y1, _ = locationsOfInterest[sub]
                _, x2, y2, _ = locationsOfInterest[sub - 2]
                _, x3, y3, _ = locationsOfInterest[sub + 4]

            elif sub in [9, 10]:
                _, x1, y1, _ = locationsOfInterest[sub]
                _, x2, y2, _ = locationsOfInterest[sub - 2]
                _, x3, y3, _ = locationsOfInterest[sub - 8]

            #
            angle = abs(atan2(y3 - y2, x3 - x2) - atan2(y1 - y2, x1 - x2))
            angle = int(angle * 180 / pi)

            if angle > 180:
                # The joints will never bend the opposite way,
                # so this prevents the program from giving you an angle greater than 180
                angle = 180 - (angle - 180)

            if sub % 2 == 0:
                rightAngles.append((sub, angle, locationsOfInterest[sub - 2][3]))
            else:
                leftAngles.append((sub, angle, locationsOfInterest[sub - 2][3]))

            # Display the angles on screen
            if showText is True:
                img = displayText(img, str(angle), (x2, y2), 2, (255, 0, 0))

        except TypeError:
            pass

    # The left and right angles list have some elements switched around here to flow as follows:
    # Elbow, Shoulder, Hip, Knee
    # This allows me to label these point in this order:
    # Left Angles: 1, 3, 9, 7
    # Right Angles: 2, 4, 10, 8

    # print("Here")
    try:
        switch = leftAngles[-1], rightAngles[-1]

        leftAngles.pop()
        rightAngles.pop()

        leftAngles.insert(-1, switch[0])
        rightAngles.insert(-1, switch[1])

        return img, leftAngles, rightAngles

    except IndexError:
        pass


# _____________________________________________________________________________
def checkVisibility(leftVisibility: list, rightVisibility: list):
    leftShoulder = leftVisibility[0][2]
    leftElbow = leftVisibility[1][2]
    # leftWrist = leftVisibility
    leftHip = leftVisibility[2][2]
    leftKnee = leftVisibility[3][2]
    # leftAnkle = leftVisibility
    leftVisibility = [leftShoulder, leftElbow, leftHip, leftKnee]

    rightShoulder = rightVisibility[0][2]
    rightElbow = rightVisibility[1][2]
    # rightWrist = rightVisibility
    rightHip = rightVisibility[2][2]
    rightKnee = rightVisibility[3][2]
    # rightAnkle = rightVisibility
    rightVisibility = [rightShoulder, rightElbow, rightHip, rightKnee]

    visibility = [[], []]
    for left in leftVisibility:
        if left > .85:
            visibility[0].append(True)
        else:
            visibility[0].append(False)

    for right in rightVisibility:
        if right > .85:
            visibility[1].append(True)
        else:
            visibility[1].append(False)

    # print(visibility)
    return visibility


# _____________________________________________________________________________
def trackMovement(num, xcor, ycor):
    # Nose, leftShoulder, leftElbow, leftWrist, rightShoulder, rightElbow, rightWrist,
    # leftHip, leftKnee, leftAnkle, rightHip, rightKnee, rightAnkle
    if num == 0:
        pass

    # checks the distance between nodes to look for reps
    # tracked[""].append()


# _____________________________________________________________________________
class Exercise:
    def __init__(self, name,
                 lelbow, lpit, lhip, lknee,
                 relbow, rpit, rhip, rknee,
                 mirrored=False,
                 specificPositioning=False):
        self.name = name
        self.leftAngles = [lelbow, lpit, lhip, lknee]
        self.rightAngles = [relbow, rpit, rhip, rknee]
        self.mirrored = mirrored
        self.specific = specificPositioning

    def exerciseLeftAngles(self):
        return self.leftAngles

    def exerciseRightAngles(self):
        return self.rightAngles


bicepCurls = Exercise("BicepCurls",
                      (0, 110, 75), (0, 45, 45), (120, 180, 180), (120, 180, 180),
                      (0, 110, 75), (0, 45, 45), (120, 180, 180), (120, 180, 180),
                      True)
singleArmBicepCurls = Exercise("SingleArmBicepCurls",
                               (0, 110, 75), (0, 45, 45), (120, 180, 180), (120, 180, 180),
                               (0, 110, 75), (0, 45, 45), (120, 180, 180), (120, 180, 180)
                               )
barbellSquats = Exercise("barbellSquats",
                         (0, 70, 70), (0, 70, 70), (0, 100, 70), (0, 100, 70),
                         (0, 70, 70), (0, 70, 70), (0, 100, 70), (0, 100, 70),
                         True
                         )
gobletSquats = Exercise("gobletSquats",
                        (0, 25, 25), (0, 25, 25), (0, 100, 70), (0, 100, 70),
                        (0, 25, 25), (0, 25, 25), (0, 100, 70), (0, 100, 70),
                        True
                        )

exercises = {bicepCurls: [bicepCurls.exerciseLeftAngles(),
                          bicepCurls.exerciseRightAngles()],
             singleArmBicepCurls: [singleArmBicepCurls.exerciseLeftAngles(),
                                   singleArmBicepCurls.exerciseRightAngles()],
             barbellSquats: [barbellSquats.exerciseLeftAngles(),
                             barbellSquats.exerciseRightAngles()],
             gobletSquats: [gobletSquats.exerciseLeftAngles(),
                            gobletSquats.exerciseRightAngles()]}


# _____________________________________________________________________________
def detectExercise(leftAngles, rightAngles, loc):
    print("\nDetecting")
    # presetExerciseAngles = []
    # Exercises listed below have 2 lists. These lists correlate to the major and minor angles list;
    # When the computer checks for the exercises, it will loop through the list and append that to another loop#
    potentialExercises = []
    mirrored = {}
    angles = leftAngles, rightAngles
    for exercise in exercises:
        # The first [] takes you to either the:
        # exerciseLeftAngles list: [0] or
        # exerciseRightAngles list [1]
        # The second [] takes you to the specific angle range for each exercise:
        # Elbow Angle Range: [0]
        # Shoulder Angle Range: [1]
        # Hip Angle Range: [2]
        # Knee Angle Range: [3]
        # The third [] takes you to the:
        # Minimum range: [0]
        # Maximum range: [1]
        try:
            mirrored[exercise.name] = [False, False]
            for sub in range(2):
                if (exercises[exercise][sub][0][0] <= angles[sub][0][1] <= exercises[exercise][sub][0][1] and
                        exercises[exercise][sub][1][0] <= angles[sub][1][1] <= exercises[exercise][sub][1][1] and
                        exercises[exercise][sub][2][0] <= angles[sub][2][1] <= exercises[exercise][sub][2][1] and
                        exercises[exercise][sub][3][0] <= angles[sub][3][1] <= exercises[exercise][sub][3][1]):
                    mirrored[exercise.name][sub] = True
                    if exercise not in potentialExercises:
                        potentialExercises.append(exercise)
        except IndexError:
            pass

    for exer in potentialExercises:
        a, b = mirrored[exer.name]
        if exer.mirrored is True:
            if a == b:
                pass
            else:
                potentialExercises.remove(exer)

        else:
            if a == b:
                potentialExercises.remove(exer)
            else:
                pass

    # Right wrist has to be to the right of the shoulder and within a certain height
    # Left wrist has to be to the left of the shoulder and within a certain height

    # If the distance between the wrists and the shoulder is greater than
    # the distance between the wrist and the middle of the chest then squats
    # #
    # Right wrist 15
    # Right Elbow 13
    # Right Shoulder 11
    # Left wrist 16
    # Left Elbow 14
    # Left Shoulder 12
    # print(loc[15][1], loc[11][1], loc[16][1], loc[12][1])
    if loc[13][1] > loc[11][1] > loc[15][1] and loc[14][1] < loc[12][1] < loc[16][1]:
        if gobletSquats.exerciseLeftAngles()[1][0] < angles[0][0][1] < gobletSquats.exerciseLeftAngles()[1][1] and \
                gobletSquats.exerciseRightAngles()[1][0] < angles[1][0][1] < gobletSquats.exerciseRightAngles()[1][1]:
            return gobletSquats.name
    elif loc[15][1] > loc[13][1] > loc[11][1] and loc[16][1] < loc[14][1] < loc[12][1]:
        if barbellSquats.exerciseLeftAngles()[1][0] < angles[0][0][1] < barbellSquats.exerciseLeftAngles()[1][1] and \
                barbellSquats.exerciseRightAngles()[1][0] < angles[1][0][1] < barbellSquats.exerciseRightAngles()[1][1]:
            return barbellSquats.name

    try:
        exName = potentialExercises[0]
        exName = exName.name
        print(exName)
        return exName
    except IndexError:
        pass


# _____________________________________________________________________________
def detectRepetitions(confirmedExercise, leftAngles, rightAngles):
    print("Detect Reps")
    print(confirmedExercise)
    try:
        currentAngle = leftAngles, rightAngles
        targetAngle = exercises[confirmedExercise]

        print(currentAngle, "\n", targetAngle)
        print("Left", currentAngle[0][0][1], "Right", currentAngle[1][0][1], targetAngle[0][0][2], "\n",
              "Left", currentAngle[0][1][1], "Right", currentAngle[1][1][1], targetAngle[0][1][2], "\n",
              "Left", currentAngle[0][2][1], "Right", currentAngle[1][2][1], targetAngle[0][2][2], "\n",
              "Left", currentAngle[0][3][1], "Right", currentAngle[1][3][1], targetAngle[0][3][2])

        # This loop will go through a value of 0 and 1:
        # At 0 we enter the check for the left targetAngle angles
        # At 1 we enter the check for the right targetAngle angles
        # The "exercises" dictionary contains the targetAngle angle in the 3 location to make things easy;
        # The currentAngle gives the [location, Angle, visibility], so we take the second value
        # We then compare these 2 values
        anglesSatisfied = [False, False]
        for sub in range(2):
            if currentAngle[sub][0][1] <= targetAngle[sub][0][2] and \
                    currentAngle[sub][1][1] <= targetAngle[sub][1][2] and \
                    currentAngle[sub][2][1] <= targetAngle[sub][2][2] and \
                    currentAngle[sub][3][1] <= targetAngle[sub][3][2]:
                if sub == 0:
                    anglesSatisfied[0] = True
                else:
                    anglesSatisfied[1] = True

        if anglesSatisfied is True:
            return True
        else:
            return False

    except KeyError:
        pass


# _____________________________________________________________________________
def displayText(img, txt, location: tuple, size=1, color=(255, 0, 0), thickness=3):
    cv2.putText(img, txt, location, cv2.FONT_HERSHEY_PLAIN, size, color, thickness)
    return img


# _____________________________________________________________________________
def fps(img, pTime):
    try:
        cTime = time()
        frames = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(frames)), (30, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
    except ZeroDivisionError:
        pass
    return pTime


# _____________________________________________________________________________
def terminateWindows(video):
    video.release()
    cv2.destroyAllWindows()


# _____________________________________________________________________________
# _____________________________________________________________________________
def objetDetection():
    return

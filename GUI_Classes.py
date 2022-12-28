from threading import currentThread
from speechFunct import analyzeResponse
from dataBase import database
from sys import argv, exit as Exit
from cameraFunct import cvtColor, COLOR_BGR2RGB, error, fps, imshow, mp, readImg, time, VideoCapture as VC, waitKey
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread 
from PyQt5.QtGui import QImage, QPixmap

# The variables below change the window size and location for all of the created windows 
winXPos, winYPos = 0, 0
winLength, winHeight = 1080, 640
    

class Login(QWidget):
    # The pyqtSignal declarations in each class allow for specified windows to be opened
    switchToSignInWindow, switchToSignUpWindow = pyqtSignal(), pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Login')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()
    
        self.signInButton = QPushButton('Sign In')
        self.signInButton.clicked.connect(self.goToSignInWindow)

        self.signUpButton = QPushButton('Sign Up')
        self.signUpButton.clicked.connect(self.goToSignUpWindow)

        self.exitButton = QPushButton('Exit Program')
        self.exitButton.clicked.connect(self.goToExit)

        # List variable that hold all of the widegts that need to be added into the current window then adds them
        self.addToLayout = [(self.signUpButton, 0, 0, 1, 1), (self.signInButton, 0, 1, 1, 1), 
                            (self.exitButton, 1, 0, 1, 2)]
        for x in self.addToLayout:
            layout.addWidget(x[0], x[1], x[2], x[3], x[4])
        self.setLayout(layout)

    def goToSignInWindow(self):
        self.switchToSignInWindow.emit()

    def goToSignUpWindow(self):
        self.switchToSignUpWindow.emit()

    def goToExit(self):
        exit("Thank You! \nDo Come Again")

class SignIn(QWidget):
    switchToMenuWindow, switchToLoginWindow = pyqtSignal(), pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Sign In')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()

        self.userNameLabel = QLabel("Username")
        self.userNameTB = QLineEdit()
        self.passwordLabel = QLabel("Password")
        self.passwordTB = QLineEdit()


        self.backButton = QPushButton('Back To Login Page')
        self.backButton.clicked.connect(self.goToLoginWindow)

        self.submitButton = QPushButton('Submit')
        self.submitButton.clicked.connect(self.goToMenuWindow)

        self.addToLayout = [(self.userNameLabel, 0, 0, 1, 1), (self.userNameTB, 0, 1, 1, 1), (self.passwordLabel, 0, 2, 1, 1), (self.passwordTB, 0, 3, 1, 1), 
                            (self.backButton, 1, 0, 1, 2), (self.submitButton, 1, 2, 1, 2)]
        for x in self.addToLayout:
            layout.addWidget(x[0], x[1], x[2], x[3], x[4])        
        self.setLayout(layout)

    def goToMenuWindow(self):
        uName = self.userNameTB.text()
        passW = self.passwordTB.text()
  
        if uName in database:
            if database[uName] == passW:
                self.switchToMenuWindow.emit()
        else:
            pass

    def goToLoginWindow(self):
        self.switchToLoginWindow.emit()

class SignUp(QWidget):
    switchToAccountCreationWindow, switchToLoginWindow = pyqtSignal(list), pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Sign Up')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()             

        self.firstNameLabel = QLabel("First Name")
        self.firstNameTB = QLineEdit()
        self.lastNameLabel = QLabel("Last Name")
        self.lastNameTB = QLineEdit()
        
        self.bodyTypeLabel = QLabel("Body Type")
        self.bodyTypeTB = QLineEdit()
        self.bodyWeightLabel = QLabel("Body Weight")
        self.bodyWeightTB = QLineEdit()

        self.submitButton = QPushButton('Submit')
        self.submitButton.clicked.connect(self.goToAccountCreationWindow)      

        self.backButton = QPushButton('Back To Login Page')
        self.backButton.clicked.connect(self.goToLoginWindow)

        self.addToLayout = [(self.firstNameLabel, 0, 0, 1, 1), (self.firstNameTB, 0, 1, 1, 1), 
                            (self.lastNameLabel, 1, 0, 1, 1), (self.lastNameTB, 1, 1, 1, 1), 
                            (self.bodyTypeLabel, 2, 0, 1, 1), (self.bodyTypeTB, 2, 1, 1, 1), 
                            (self.bodyWeightLabel, 3, 0, 1, 1), (self.bodyWeightTB, 3, 1, 1 ,1),
                            (self.backButton, 4, 0, 1, 1), (self.submitButton, 4, 1, 1, 1)]

        for x in self.addToLayout:
            layout.addWidget(x[0], x[1], x[2], x[3], x[4])
        self.setLayout(layout)
    
    def goToAccountCreationWindow(self):
        self.switchToAccountCreationWindow.emit([x.text() for x in self.addToLayout])

    def goToLoginWindow(self):
        self.switchToLoginWindow.emit()


class AccountCreationWindow(QWidget):
    switchToMenuWindow, switchToSignUpWindow = pyqtSignal(), pyqtSignal()

    def __init__(self, genUserInfo):
        QWidget.__init__(self)
        self.setWindowTitle('Sign Up')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()             

        self.genUserInfo = genUserInfo
        self.userNameTB = QLineEdit()
        self.passwordTB = QLineEdit()

        self.submitButton = QPushButton('Submit')
        self.submitButton.clicked.connect(self.goToMenuWindow) 

        self.backButton = QPushButton('Back To Sign Up Page')
        self.backButton.clicked.connect(self.goToSignUpWindow)

        self.addToLayout = [self.userNameTB, self.passwordTB, self.submitButton, self.backButton]
        for x in self.addToLayout:
            layout.addWidget(x)
        self.setLayout(layout)
    
    def goToMenuWindow(self):
        # The credentials that the User enters will be checked in this method
        # To do they will have to enter a username and password that has not been entered into the database
        uName = self.userNameTB.text()
        passW = self.passwordTB.text()
        
        try: 
            # The entered Username is compared to other Usernames in the data base
            if uName not in database: 
                newPass = True
                # Here, every saved Password is then checked against the Password the current user has entered
                for x in database:
                    if passW == database[x]:
                        newPass = False
                # If the credentials entered by the user does not match any in the database,
                #  the varaiable "newPass" will remain True and the new Account is granted access 
                if newPass is True:
                    self.switchToMenuWindow.emit()                
        except KeyError:
            pass

    def goToSignUpWindow(self):
        self.switchToSignUpWindow.emit()


class MainMenuWindow(QWidget):
    switchToChatBotWindow, switchToWorkoutWindow, switchToLoginWindow = pyqtSignal(), pyqtSignal(), pyqtSignal() 

    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('Main Window')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()

        self.chatBotButton = QPushButton('Chat With Workout Assistant')
        self.chatBotButton.clicked.connect(self.goToChatBotWindow)

        self.workoutButton = QPushButton('Workout Window')
        self.workoutButton.clicked.connect(self.goToWorkoutWindow)

        self.exitButton = QPushButton('Exit Program')
        self.exitButton.clicked.connect(self.goToExit)

        self.addToLayout = [self.chatBotButton, self.workoutButton, self.exitButton]
        for x in self.addToLayout:
            layout.addWidget(x)
        self.setLayout(layout)

    def goToChatBotWindow(self):
        self.switchToChatBotWindow.emit()

    def goToWorkoutWindow(self):
        self.switchToWorkoutWindow.emit()

    def goToExit(self):
        exit("Thank You! \nDo Come Again")



class ChatBotWindow(QWidget):
    switchToMenuWindow = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.CONTEXT = None

        self.setWindowTitle('ChatBot')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()

        self.userMessageHistory1 = QLabel("_____")
        self.userMessageHistory2 = QLabel("_____")
        self.userMessageHistory3 = QLabel("_____")
        
        self.chatBotMessageHistory1 = QLabel("_____")
        self.chatBotMessageHistory2 = QLabel("_____")
        self.chatBotMessageHistory3 = QLabel("_____")

        self.userInput = QLineEdit()
        self.userInput.returnPressed.connect(self.goToAskChatBot)


        self.backButton = QPushButton('Back To Menu')
        self.backButton.clicked.connect(self.goToMenuWindow)
        self.enterButton = QPushButton('Enter')
        self.enterButton.clicked.connect(self.goToAskChatBot)
        
        self.borderLeft = QLabel("BderL")
        self.borderRight = QLabel("BderR")

        #self.addToLayout = [(self., 0, 0, 1, 1)]
        #for x in self.addToLayout:
        #    layout.addWidget(x, 0, 0, 1, 1)
        #self.setLayout(layout)
        
        layout.addWidget(self.borderLeft, 0, 0, 3, 1)
        layout.addWidget(self.borderRight, 0, 3, 4, 1)

        layout.addWidget(self.userMessageHistory3, 1, 1)
        layout.addWidget(self.userMessageHistory2, 2, 1)
        layout.addWidget(self.userMessageHistory1, 3, 1)

        layout.addWidget(self.chatBotMessageHistory3, 1, 2)
        layout.addWidget(self.chatBotMessageHistory2, 2, 2)
        layout.addWidget(self.chatBotMessageHistory1, 3, 2)

        layout.addWidget(self.userInput, 4, 1, 1, 2)
        layout.addWidget(self.backButton, 4, 0)
        layout.addWidget(self.enterButton, 4, 3)

        self.setLayout(layout)
    
    def goToMenuWindow(self):
        self.switchToMenuWindow.emit()

    def goToAskChatBot(self):
        self.userMessageHistory3.setText(self.userMessageHistory2.text())
        self.userMessageHistory2.setText(self.userMessageHistory1.text())
        
        self.chatBotMessageHistory3.setText(self.chatBotMessageHistory2.text())
        self.chatBotMessageHistory2.setText(self.chatBotMessageHistory1.text())
        
        self.userMessageHistory1.setText(self.userInput.text())
        response, self.CONTEXT = analyzeResponse(self.userInput.text(), self.CONTEXT)
        self.chatBotMessageHistory1.setText(response)

        self.userInput.clear()
        

workoutAngles = None
currentWorkout = None
class WorkoutWindow(QWidget):
    switchToMenuWindow = pyqtSignal()

    def __init__(self):
        global workoutAngles
        QWidget.__init__(self)
        self.setWindowTitle('Workout Window')
        self.setGeometry(winXPos, winYPos, winLength, winHeight)

        layout = QGridLayout()

        self.videoLabel = QLabel(self)
        #self.videoLabel.move(280, 120)
        #self.videoLabel.resize(640, 480)
        th = Thread()
        th.changePixmap.connect(self.captureImage)
        th.start()
        #self.show()

        workoutAngles = QLabel("____")
        currentWorkout = QLabel("____")

        self.userInput = QLineEdit()
        self.userInput.returnPressed.connect(self.goToAskChatBot)

        self.backButton = QPushButton('Back To Menu')
        self.backButton.clicked.connect(self.goToMenuWindow)

        self.addToLayout = [(self.videoLabel, 0, 0, 1, 4),
                            (workoutAngles, 1, 0, 1, 2), (currentWorkout, 1, 1, 1, 2),
                            (self.backButton, 2, 0, 1, 1)]
        
        for x in self.addToLayout:
            layout.addWidget(x, 0, 0, 1, 1)
        self.setLayout(layout)
        
        layout.addWidget(self.videoLabel, 0, 0)
        layout.addWidget(workoutAngles, 1, 0)
        layout.addWidget(self.backButton, 2, 0)

        self.setLayout(layout)
    
    def captureImage(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))        

    def goToMenuWindow(self):
        self.switchToMenuWindow.emit()


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        global defaultCam
        self.defaultCam = defaultCam

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
        exName = None

        downTime = 5
        currentDownTime = time()
        # firstTimeCheckBool = True
        minimumRepCount = 1
    
        xLength = 720
        yHeight = 480
        if self.defaultCam == 0:
            video = VC(0)
        elif self.defaultCam == (0, 1):
            print("Okay")
            video = VC(1)
        elif self.defaultCam == 1:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test1.gif")  # Single Arm Bicep Curl
        elif self.defaultCam == 2:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test2.mp4")  # Bicep Curl 2
        elif self.defaultCam == 3:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test3.gif")  # Bicep Curls  need new
        elif self.defaultCam == 4:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test4.gif")  # Squat
        elif self.defaultCam == 5:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test5.gif")  # Back Squat 2
        elif self.defaultCam == 6:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test6.gif")  # Squat 3  need new
        elif self.defaultCam == 7:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test7.gif")  # Front Squats
        elif self.defaultCam == 8:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test8.gif")  # Front Squats
        elif self.defaultCam == 9:
            video = VC("C:\\Users\\Big Boi J\\Downloads\\test9.gif")


        video.set(3, xLength)
        video.set(4, yHeight)

        global workoutAngles
        global currentWorkout

        while True: 
            try:
                returned, img, assumption2, exName, \
                repCompleted, trackedAngles, \
                allLocations = readImg(video, pose, drawLM, exName,
                                       showInterest=True, showDots=False,
                                       showLines=True, showText=True, known=known,
                                       confirmedExercise=confirmedExercise)
                
                workoutAngles.setText(repCompleted[1])
                currentWorkout.setText()
                
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
            except RuntimeError:
                break

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
                #imshow("Picture", img)
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

            if returned:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cvtColor(img, COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(winLength - 150, winHeight - 150, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class Controller:

    def __init__(self):
        pass

    def showLogin(self):
        try:
           self.signIn.close()
        except:
            pass
        try:
           self.signUp.close()
        except:
            pass
        
        self.login = Login()
        self.login.switchToSignInWindow.connect(self.showSignIn)
        self.login.switchToSignUpWindow.connect(self.showSignUp)
        self.login.show()

    def showSignIn(self):
        try:
           self.login.close()
        except:
            pass

        self.signIn = SignIn()
        self.signIn.switchToMenuWindow.connect(self.showMainMenu)
        self.signIn.switchToLoginWindow.connect(self.showLogin)
        self.signIn.show()

    def showSignUp(self):
        try:
           self.login.close()
        except:
            pass
        try:
           self.accountCreation.close()
        except:
            pass

        self.signUp = SignUp()
        self.signUp.switchToAccountCreationWindow.connect(self.showAccountCreation)
        self.signUp.switchToLoginWindow.connect(self.showLogin)
        self.signUp.show()

    def showAccountCreation(self, genUserInfo):
        try:
           self.signUp.close()
        except:
            pass

        self.accountCreation = AccountCreationWindow(genUserInfo)
        self.accountCreation.switchToMenuWindow.connect(self.showMainMenu)
        self.accountCreation.switchToSignUpWindow.connect(self.showSignUp)
        self.accountCreation.show()


    def showMainMenu(self):
        # This doesn't work??
        #windowsToClose = [self.signIn, self.signUp, self.chatBot, self.workOut]

        #for window in windowsToClose:
        #    try:
        #        window.close()
        #    except AttributeError:
        #        pass

        try:
           self.signIn.close()
        except:
            pass
        try:
           self.signUp.close()
        except:
            pass
        try:
           self.accountCreation.close()
        except:
            pass
        try:
           self.chatBot.close()
        except:
            pass
        try:
           self.workOut.close()
        except:
            pass
        
        self.mainMenuWindow = MainMenuWindow()
        self.mainMenuWindow.switchToChatBotWindow.connect(self.showChatBot)
        self.mainMenuWindow.switchToWorkoutWindow.connect(self.showWorkout)
        
        self.mainMenuWindow.show()

    def showChatBot(self):
        try:
            self.mainMenuWindow.close()
        except AttributeError:
            pass

        self.chatBot = ChatBotWindow()
        self.chatBot.switchToMenuWindow.connect(self.showMainMenu)
        self.chatBot.show()

    def showWorkout(self):
        try:
            self.mainMenuWindow.close()
        except AttributeError:
            pass

        self.workOut = WorkoutWindow()
        self.workOut.switchToMenuWindow.connect(self.showMainMenu)
        self.workOut.show()


def main():
    app = QApplication(argv)
    controller = Controller()
    
    #controller.showLogin()
    controller.showSignIn()
    #controller.showSignUp()
    #controller.showAccountCreation()
    #controller.showMainMenu()
    #controller.showChatBot()
    #controller.showWorkout()
    Exit(app.exec_())


defaultCam = 3
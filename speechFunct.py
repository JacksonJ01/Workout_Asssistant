# # This file will contain the functions for the Speech Recognition and Response
# from nltk import word_tokenize
# from numpy import array
from re import split
from random import randrange
from speech_recognition import Recognizer, Microphone, UnknownValueError
from pyttsx3 import init
from socket import gethostname as ghn


# from random import choice
#


def talkOrText(com=None):
    if com is None:
        com = input("\n1. Talk"
                    "\n2. Text"
                    "\n>>>")
    try:
        if com == 1:
            return True
        elif com == 2:
            return False
        else:
            raise ValueError
    except ValueError:
        return False


def listeningToUser(talk=False):
    if talk is True:
        mic = Recognizer()
        with Microphone() as _source:
            _audio = mic.listen(_source)
        try:
            print("Speak Now...")
            # Needs to have a wake word
            audioText = mic.recognize_google(_audio)
            return audioText
        except UnknownValueError:
            return False

    elif talk is False:
        # text = input("Type Your Message:"
        #              "\nYou>>>")
        # return text
        try:
            text = input("\nType Your Message:"
                         "\nYou>>>")
            return text
        except EOFError:
            pass



def analyzeResponse(userInput, context):
    #print(userInput)
    for x in userInput:
        if f"{x}".isalpha() is False and f"{x}".isdigit() is False and x != " ":
            userInput = f"{userInput}".replace(f"{x}", "")
    # print(userInput)
    # print("Here1")
    response, context = checkMessage(userInput.lower(), context)
    return response, context


# edit this function to allow context messages
def checkMessage(userInput: str, contextFiltered=None):
    # print("In", contextFiltered)
    highestProbability = {}
    contextSet = {}
    minimumTime = 5

    def response(chatBotResponse, listOfWords, singleResponse=False,
                 requiredWords=[], userIn=userInput.lower(), filtering=None, filtered=None):
        # print("Here2")
        nonlocal highestProbability
        nonlocal contextSet

        userIn = split(r"\s+|[ ]\s+", f"{userIn}".lower())
        if contextFiltered is not None:
            if filtered == contextFiltered:
                # Chooses one of the responses for the list of choices
                chatBotResponse = chatBotResponse[randrange(len(chatBotResponse))]
                highestProbability[chatBotResponse] = messageProbability(userIn, listOfWords, singleResponse, requiredWords)

                if filtering is not None:
                    contextSet[chatBotResponse] = filtering
        else:
            # Chooses one of the responses for the list of choices
            chatBotResponse = chatBotResponse[randrange(len(chatBotResponse))]
            highestProbability[chatBotResponse] = messageProbability(userIn, listOfWords, singleResponse, requiredWords)
            contextSet[chatBotResponse] = filtering

    if contextFiltered == ("start timer"):
        try:
            # To get the numbers from the userInput
            amountOfTime = [int(length) for length in userInput.split() if length.isdigit()]
            # print(amountOfTime)
            if not amountOfTime:
                return unknown(), None
            unit = ""
            # if amountOfTime[0] == 1:
            #     if "second" in userInput:
            #         # unit = "seconds"  # sets the timer to second
            #         return "You are unable to set a timer for 1 second", "start timer"
            #     if "minute" in userInput:
            #         unit = "minute"  # sets the timer to minute
            #     if "hour" in userInput:
            #         unit = "hour"  # sets the timer to hour
            # else:
            if "second" in userInput:
                if amountOfTime[0] < minimumTime:
                    return f"You are unable to set a timer under {minimumTime} seconds\n", "start timer"
                unit = "seconds"  # sets the timer to seconds
            if "minute" in userInput:
                unit = "minutes"  # sets the timer to minutes
            if "hour" in userInput:
                unit = "hours"  # sets the timer to hours

            return f"Starting Timer For {amountOfTime[0]} {unit}\n", None

        except ValueError:
            unknown()
        except IndexError:
            unknown()

    ##################################
    #if contextfiltered == "":
    #    pass

    #if contextfiltered == "":
        pass

    # Greeting
    response(["Hello", "Hi", "Hello there"],
             ["hello", "sup", "hey", "heyo", "hi"],
             singleResponse=True)

    response(["Maybe, what's up", 
              "Yes, at the ready", 
              "Mmm, depends on who's askin"],
             ["where", "are", "you", "there"],
             requiredWords=["are", "you", "there"])

    response(["I'm doing well, and you?",
              "Great, and you?"],
             ["how", "are", "you", "doing"],
             requiredWords=["how", "are", "you"],
             filtering="extendedGreeting")

    response(["That's good to hear", "That's great", "Nice!"],
             ["i", "am", "good", "great", "awesome", "amazing", "happy"],
             requiredWords=["i", "am"],
             filtered="extendedGreeting")

    response(["Awe, I wish I could help more",
              "Sorry to hear that",
              "Hopefully things get better"],
             ["i", "am", "sad", "bad", "mad", "unhappy"],
             requiredWords=["i", "am"],
             filtered="extendedGreeting")

    # Identity Questions
    response([f"I am {ghn()}",
              "Your personal assistant",
              "Call me what you'd like"],
             ["who", "are", "you"],
             requiredWords=["who", "are", "you"])

    response(["I am magical", "A brilliant mind made me",
              "I'm just a computer..", "Great question!"],
             ["how", "do", "you", "work"],
             requiredWords=["how", "do", "you", "work"])

    #response(["", "", ""],
    #         ["", "", "", ""],
    #         requiredWords=["", ""])

    # Start Timer
    response(["How long? (Number and Unit Of Time)",
              "What length of time would you like? "
              "(Number and Unit Of Time)",
              "For how long? (Number and Unit Of Time)"],
             ["start", "a", "timer"],
             requiredWords=["start", "timer"],
             filtering="start timer")

    # Pause Timer
    response(["Pausing Timer"],
             ["pause", "timer"],
             requiredWords=["pause", "timer"])

    # Resume Timer
    response(["Resuming Timer"],
             ["resume", "timer"],
             requiredWords=["resume", "timer"])

    # Stop Timer
    response(["Stopping Timer"],
             ["stop", "timer"],
             requiredWords=["end", "timer"])

    # End Timer
    response(["Ending Timer", ],
             ["end", "timer"],
             requiredWords=["end", "timer"])

    # Cancel Timer
    response(["Cancelling Timer"],
             ["cancel", "timer"],
             requiredWords=["cancel", "timer"])
    #
    #
    # Start Stopwatch
    response(["Okay", "Starting Stopwatch"],
             ["start", "a", "stopwatch"],
             requiredWords=["start", "stopwatch"])
    response(["Okay", "Starting Stopwatch"],
             ["start", "a", "stop", "watch"],
             requiredWords=["start", "stop", "watch"])

    # Pause Stopwatch
    response(["Pausing Stopwatch"],
             ["pause", "stopwatch"],
             requiredWords=["pause", "stopwatch"])
    response(["Pausing Stopwatch"],
             ["pause", "stop", "watch"],
             requiredWords=["pause", "stop", "watch"])

    # Resume Stopwatch
    response(["Resuming Stopwatch"],
             ["resume", "stopwatch"],
             requiredWords=["resume", "stopwatch"])
    response(["Resuming Stopwatch"],
             ["resume", "stop", "watch"],
             requiredWords=["resume", "stop", "watch"])

    # Stop Stopwatch
    response(["Stopping Stopwatch"],
             ["stop", "stopwatch"],
             requiredWords=["end", "stopwatch"])
    response(["Stopping Stopwatch"],
             ["stop", "stop", "watch"],
             requiredWords=["end", "stop", "watch"])

    # End Stopwatch
    response(["Ending Stopwatch"],
             ["end", "stopwatch"],
             requiredWords=["end", "stopwatch"])
    response(["Ending Stopwatch"],
             ["end", "stop", "watch"],
             requiredWords=["end", "stop", "watch"])

    # Cancel Stopwatch
    response(["Cancelling Stopwatch"],
             ["cancel", "stopwatch"],
             requiredWords=["cancel", "stopwatch"])
    response(["Cancelling Stopwatch"],
             ["cancel", "stop", "watch"],
             requiredWords=["cancel", "stop", "watch"])

    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])
    # response(["", "", ""],
    #          ["", "", "", ""],
    #          requiredWords=["", ""])

    # Leaving
    response(["You too", "You as well", "Have a good night"],
             ["have", "a", "great", "good", "day"],
             requiredWords=["have", "day"])

    response(["Goodbye", "See you later"],
             ["bye", "goodbye", "adios"],
             singleResponse=True)

    response("Disconnecting",
             ["disconnect", "from", "server"],
             requiredWords=["disconnect"])

    # print("Here3")
    # print(highestProbability)
    bestFit = max(highestProbability, key=highestProbability.get)

    if contextFiltered is not None:
        return bestFit, None
    else:
        # print(highestProbability)
        # print(bestFit)
        # print(contextSet.get(bestFit))
        return unknown() if highestProbability[bestFit] < 1 else bestFit + "\n", contextSet.get(bestFit)


def messageProbability(userInput, recognisedWords, singleResponse=False, requiredWords=[]):
    messageCertainty = 0
    hasRequiredWords = True

    for word in userInput:
        if word in recognisedWords:
            messageCertainty += 1

    percentage = float(messageCertainty) / float(len(recognisedWords))

    for word in requiredWords:
        if word not in userInput:
            hasRequiredWords = False
            break

    if hasRequiredWords or singleResponse:
        return int(percentage * 100)
    else:
        return 0


def unknown():
    response = ["Can you repeat or re-phrase that?",
                "Unable to process",
                "Try again",
                "What do you mean?"][randrange(4)]
    return response + "\n"


def textToSpeech(_text):
    speaker = init()
    speaker.say(_text)
    speaker.runAndWait()
    return _text

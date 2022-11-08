from speechFunct import talkOrText, listeningToUser, analyzeResponse, textToSpeech
# from client import ClientMessaging
from multiprocessing import Queue
from time import sleep as s

chatMode = 2


def chatBot(_context=None): #, queue: Queue = None):
    talk = talkOrText(chatMode)
    if talk is True:
        textToSpeech("Chat Bot is Listening")
    elif talk is False:
        print("ChatBot: Listening")

    # while True:
        # s(2)
    try:
        userInput = listeningToUser(talk).strip()
        bestFit, context = analyzeResponse(userInput, _context)
        _context = context

        # if queue is not None:
        #     msg = queue.get()
        #     msg["Message"] = [bestFit, _context]
        #     queue.put(msg)

        if talk is True:
            return textToSpeech(bestFit), _context
        elif talk is False:
            return bestFit, _context
    except AttributeError:
        pass


_context = None
# client = ClientMessaging

# while True:
#     response, _context = chatBot(_context)
#     print("Response:", response, "\n") if response != "Disconnecting" else quit("Disconnected")
#     # try:
#     #     # client.sendServerMessage(response)
#     # except ConnectionError:
#     #     pass

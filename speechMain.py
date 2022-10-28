from speechFunct import talkOrText, listeningToUser, analyzeResponse, textToSpeech
from client import ClientMessaging

chatMode = 2


def chatBot(_context=None):
    talk = talkOrText(chatMode)
    if talk is True:
        textToSpeech("Chat Bot is Listening")
    elif talk is False:
        print("ChatBot: Listening")

    while True:
        userInput = listeningToUser(talk).strip()
        bestFit, context = analyzeResponse(userInput, _context)
        _context = context

        if talk is True:
            return textToSpeech(bestFit), _context
        elif talk is False:
            return bestFit, _context


_context = None
client = ClientMessaging

while True:
    response, _context = chatBot(_context)
    print("Response:", response, "\n") if response != "Disconnecting" else quit("Disconnected")
    try:
        client.sendServerMessage(response)
    except ConnectionError:
        pass

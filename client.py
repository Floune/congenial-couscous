import socket, threading, queue
import curses
import random
from nickname import randoum
from curses import wrapper
import signal
import time
import os
import sys
from desktop_notifier import DesktopNotifier, Urgency, Button
import requests
import vlc

 
def handler(signum, frame):
    client.send("____deco".encode('utf-8'))
    curses.endwin()
    sys.exit(1)
 
signal.signal(signal.SIGINT, handler)
q = queue.Queue()
notify = DesktopNotifier()
p = vlc.MediaPlayer("https://listen.nolife-radio.com/stream")

messages = []
currentMsg = ""
colorSequence = []
nicknames = []

nickname = randoum()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(os.environ.get('FLOUNE_CHAT_SERVER', 'localhost'), os.environ.get('FLOUNE_CHAT_PORT', 5556))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            else:
                q.put(message)


        except:
            print("An error occured!")
            client.close()
            break

        
def gui():
    win = curses.newwin(21, 200, 0, 0)
    win.clear()
    win.refresh()
    while True:
        m = q.get()
        handleMessages(m)
        updateGui(win)

       
def updateGui(win):

    # notify.send_sync(
    #     title="prout",
    #     message="nouveau message ultra secret",
    #     urgency=Urgency.Critical,
    #     buttons=[
    #         Button(title="j'ai vu, fous moi la paix"),
    #     ],
    # ),

    win.move(0, 0)
    win.clear()
    win.refresh()

    for i, m in enumerate(messages):
        arr = m.split("::::")
        if len(arr) > 1 and len(arr[1]) > 0:
            colorIndex = (ord(arr[0][0]) % 5) + 1
            win.addstr(i, 0, arr[0], curses.color_pair(colorIndex))
            win.addstr(i, len(arr[0]) + 2, arr[1])
    win.refresh()

def handleMessages(message):
    global colorSequence
    global messages
    if len(messages) > 20:
        del messages[0]
        del colorSequence[0]
    colorSequence.append(random.choice(range(1, 5)))
    messages.append(message)

def handleCommand(c):
    if (c[1:] == "joke"):
        response = requests.get("https://api.chucknorris.io/jokes/random")
        client.send('{}::::{}'.format(nickname, response.json()['value']).encode("utf8"))
    elif (c[1:] == "shrug"):
        client.send('{}::::{}'.format(nickname, "¯\\_(ツ)_/¯").encode("utf8"))
    elif (c[1:] == "nolife"):
        p.play() 
    elif (c[1:] == "stop"):
        p.stop()
    else:
        client.send('{}'.format(c).encode("utf8"))

def write():
    win = curses.newwin(1, 200, 23, 0)
    win.keypad(True)
    curses.echo()
    win.clear()
    win.refresh()
    while True:
        win.move(0, 0)
        c = win.getstr(0, 0)
        decoded = c.decode('utf-8')
        if len(decoded) > 1 and decoded[0] == "/":
            handleCommand(decoded)
        else:
            message = '{}::::{}'.format(nickname, decoded)
            client.send(message.encode('utf-8'))
        win.clear()
        win.refresh()


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE),
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE),
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN),
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED),
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW),
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA),

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
    
    gui_thread = threading.Thread(target=gui)
    gui_thread.start()

wrapper(main)

import socket, threading, queue
import curses
import random
import signal
import time
import os
import sys
import requests

from curses import wrapper
from globals_ import *
from todo import *
from emojis import *
from radio import *
from activity import *
from gui import *
from datetime import datetime
#from desktop_notifier import DesktopNotifier, Urgency, Button

def handler(signum, frame):
    sys.exit(1)
    client.send("____deco".encode(encodingMethod))
    curses.endwin()

 
signal.signal(signal.SIGINT, handler)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((os.environ.get('FLOUNE_CHAT_SERVER', 'localhost'), int(os.environ.get('FLOUNE_CHAT_PORT', 5556))))

q = queue.Queue()

def receive():
    global users
    while True:
        try:
            message = client.recv(1024).decode(encodingMethod)

            if message == nicknameRequestString:
                client.send(nickname.encode(encodingMethod))
            elif nbUserRequestString in message:
                users = message.split(systemMessageSplitString)[1]
                q.put("")
            else:
                q.put(message)


        except:
            print("An error occured!")
            client.close()
            break

def gui():
    win = curses.newwin(21, 100, 0, 0)
    win.clear()
    win.refresh()
    while True:
        m = q.get()
        handleMessages(m)
        updateGui(win)

       
def displayInfos(win):
    if tabinfo == 0:
        mes = "participant" if users == "1" else "participants"
        win.move(0, 0)
        win.addstr(1, 0, "{} {}".format(users, mes))
        win.refresh()
        win.addstr(0, 0, "Connecté en tant que ")
        win.refresh()
        win.addstr(0, 22, "{}".format(nickname), curses.color_pair(7))
        win.refresh()
    elif tabinfo == 1:

        win.addstr(0, 0, "à l'écoute: {}".format(alecoute))
        win.addstr(1, 0, "volume : {}%".format(volume))
        win.refresh()


def displayMessages(win):
    for i, m in enumerate(messages):
        if (len(m.split(userMessageSplitString)) > 1 and m.split(userMessageSplitString)[1] == "") or len(m) < 1:
            del(messages[i])
        elif userMessageSplitString in m:
            userMessage(m, i, win)
        elif systemMessageSplitString in m:
            systemMessage(m, i, win)

def userMessage(m, i, win):
    arr = m.split(userMessageSplitString)     
    if len(arr) > 1:
        colorIndex = (ord(arr[0][letterColorIndex]) % 5) + 1
        win.addstr(i + 3, 0, arr[0], curses.color_pair(colorIndex))
        win.refresh()
        win.addstr(i + 3, len(arr[0]) + 2, arr[1])
        win.refresh()

def systemMessage(m, i, win):
    arr = m.split(systemMessageSplitString)        
    if len(arr) > 1:
        colorIndex = 0
        win.addstr(i + 3, 0, arr[0], curses.color_pair(colorIndex))
        win.refresh()
        win.addstr(i + 3, len(arr[0]) + 2, arr[1])
        win.refresh()

def displayTodo(win):
    win.addstr(3, 0, "TODO list", curses.color_pair(1))
    win.refresh()
    for i, todo in enumerate(todos):
        win.addstr(i + 5, 0, "{} - {}".format(i, todo["value"]), curses.color_pair(todo["color"]))
        win.refresh()

def displayTrack(win):
    win.addstr(3, 0, "Tracker", curses.color_pair(1))
    win.refresh()
    trackDisplayLoop(win, activities)


def updateGui(win):
    win.move(0, 0)
    win.clear()
    displayInfos(win)
    if activity == "chat":
        displayMessages(win)
    elif activity == "todo":
        displayTodo(win)
    elif activity == "track":
        displayTrack(win)

def handleMessages(message):
    global messages
    if len(messages) > 16:
        del messages[0]
    messages.append(message)


def handleCommand(c):
    global alecoute
    global volume
    global activities

    if c[1:] in emojisNames:
        emoj(nickname, c[1:], client)

    elif c[1:] in radioCommands:
        new = handleRadio(c[1:])
        alecoute = new[0]
        volume = new[1]

    elif c[1:] == "swagg":
        changeColor(letterColorIndex)

    elif c[1:] == "tab":
        handleTabs()


    elif "new" in c[1:]:
        addTodo(c[1:])

    elif "done" in c[1:]:
        checkTodo(c[1:])

    elif "del" in c[1:]:
        delTodo(c[1:]) 

    elif c[1:] == "todo":
        changeActivity("todo")

    elif c[1:] == "chat":
        changeActivity("chat")

    elif c[1:] == "track":
        changeActivity("track")

    elif "workon" in c[1:]:
        newActivity(c[1:])

    elif c[1:] == "jaimenti":
        activities.popitem()

    else:
        client.send('{}'.format(c).encode("utf8"))

    q.put("")

def handleTabs():
    global tabinfo
    tabinfo = tabinfo + 1 if tabinfo < 2 else 0


def changeActivity(newActivity):
    global activity
    activity = newActivity


def changeColor(index):
    global letterColorIndex
    if (index > len(nickname) - 2):
        index = 0
    if(nickname[index] == " "):
        index += 1
        changeColor(index)
    letterColorIndex += 1

def write():
    writeScreen = curses.newwin(1, 100, 22, 0)
    writeScreen.keypad(True)
    writeScreen.clear()
    writeScreen.refresh()
    curses.echo()
    while True:
        c = writeScreen.getstr(0, 0)
        decoded = c.decode(encodingMethod)
        if len(decoded) > 1 and decoded[0] == "/":
            handleCommand(decoded)
        else:
            message = '{}::::{}'.format(nickname, decoded)
            client.send(message.encode(encodingMethod))
        writeScreen.clear()
        writeScreen.refresh()


def main(stdscr):
    global activities

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE),
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE),
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN),
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED),
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW),
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK),


    maybeTodo()

    activities = maybeActivities()

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
    
    gui_thread = threading.Thread(target=gui)
    gui_thread.start()

wrapper(main)

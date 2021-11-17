import socket, threading, queue
import curses
import random
import signal
import time
import os
import sys
import requests
# import pyw3mimg

from curses import wrapper
from globals_ import *
from todo import *
from emojis import *
from radio import *
from activity import *
from gui import *
from datetime import datetime
from datetime import timedelta
from playsound import playsound
from audioclient import *

#from desktop_notifier import DesktopNotifier, Urgency, Button

def handler(signum, frame):
    abortMission()
    curses.endwin()
    sys.exit(1)
    
signal.signal(signal.SIGINT, handler)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((os.environ.get('FLOUNE_CHAT_SERVER', 'localhost'), int(os.environ.get('FLOUNE_CHAT_PORT', 5556))))
q = queue.Queue()

def receive():
    global users
    global client
    while True:
        try:
            message = client.recv(1024).decode(encodingMethod)

            if message == nicknameRequestString:
                client.send(nickname.encode(encodingMethod))
            elif nbUserRequestString in message:
                users = message.split(systemMessageSplitString)[1]
                q.put("")
            elif "SOUND" in message:
                playSound(message.split(systemMessageSplitString)[1])
            else:
                q.put(message)
        except:
            print("An error occured!")
            client.close()
            break

def playSound(filename):
    playsound("{}.mp3".format(filename))

def gui():
    global rows
    global rows
    win = curses.initscr()
    rows, cols = win.getmaxyx()
    win.clear()
    win.refresh()
    while True:
        m = q.get()
        handleMessages(m)
        updateGui(win)

       
def displayInfos(win):
    odio = "activé" if audioMode == True else "désactivé"
    if tabinfo == 0:
        mes = "participant" if users == "1" else "participants"
        win.move(0, 0)
        win.addstr(2, 0, "radio: {} | volume : {}%".format(alecoute, volume))
        win.refresh()
        win.addstr(3, 0, "{}".format(songTitle))
        win.refresh()
        win.addstr(1, 0, "{} {}".format(users, mes))
        win.refresh()
        win.addstr(0, 0, "Connecté en tant que ")
        win.refresh()
        win.addstr(0, 22, "{}".format(nickname), curses.color_pair(7))
        win.refresh()
        win.addstr(0, 23 + len(nickname), "vocal {}".format(odio))
        win.refresh()
    elif tabinfo == 1:
        win.addstr(0, 0, "radio: {}".format(alecoute))
        win.refresh()
        win.addstr(2, 0, "{}".format(songTitle))
        win.refresh()
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
        win.refresh()


def userMessage(m, i, win):
    arr = m.split(userMessageSplitString)     
    if len(arr) > 1:
        colorIndex = (ord(arr[0][letterColorIndex]) % 5) + 1
        win.addstr(i + messageYOffset, 0, arr[0], curses.color_pair(colorIndex))
        win.addstr(i + messageYOffset, len(arr[0]) + 2, arr[1])

def systemMessage(m, i, win):
    arr = m.split(systemMessageSplitString)        
    if len(arr) > 1:
        colorIndex = 0
        win.addstr(i + messageYOffset, 0, arr[0], curses.color_pair(colorIndex))
        win.addstr(i + messageYOffset, len(arr[0]) + 2, arr[1])

def displayTodo(win):
    win.addstr(5, 0, "TODO list", curses.color_pair(1))
    win.refresh()
    for i, todo in enumerate(todos):
        win.addstr(i + messageYOffset + 2, 0, "{} - {}".format(i, todo["value"]), curses.color_pair(todo["color"]))
    win.refresh()

def displayTrack(win):
    win.addstr(5, 0, "Tracker", curses.color_pair(1))
    win.refresh()
    trackDisplayLoop(win, activities)

def displayImageBoard(win):
    win.clear()
    # outputt = repr(climage.convert('test.jpeg', width=20, is_unicode=True))
    # win.addstr("{}".format(outputt))
    # display = pyw3mimg.W3MImageDisplay()
    # display.draw('/home/floune/dev/fun/ultrachat/test.jpeg', n=1, x=0, y=0)
    win.refresh()

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
    elif activity == "board":
        displayImageBoard(win)

def handleMessages(message):
    global messages
    if len(messages) > rows - 11:
        del messages[0]
    messages.append(message)


def handleCommand(c):
    global alecoute
    global volume
    global songTitle
    global activities

    command = c[1:]
    if command in emojisNames:
        emoj(nickname, command, client)

    elif command == "song":
        songTitle = updateSongTitle()

    elif command in radioCommands:
        new = handleRadio(command)
        alecoute = new[0]
        songTitle = new[1]

    elif command == "u" or command == "d":
        volume = setVolume(command)

    elif command == "swagg":
        changeColor(letterColorIndex)

    elif command == "tab":
        handleTabs()


    elif "new" in command:
        addTodo(command)

    elif "done" in command:
        checkTodo(command)

    elif "del" in command:
        delTodo(command) 

    elif command == "todo":
        changeActivity("todo")

    elif command == "chat":
        changeActivity("chat")

    elif command == "track":
        changeActivity("track")

    elif "workon" in command:
        newActivity(command)

    elif command == "jaimenti":
        activities.popitem()

    elif command == "prout":
        client.send('{}'.format(c).encode("utf8"))

    elif command == "board":
        changeActivity("board")

    elif command == "pomodoro":
        startPomodoro()

    elif command == "vocal":
        handleVocal()
    
    else:
        client.send('{}'.format(c).encode("utf8")) #commande gérée par le serveur

    q.put("")


def handleVocal():
    global audioMode
    global audioClient
    global std
    if audioMode == False:
        audioMode = True
        curses.savetty()
        run()
        q.put('')
    else:
        abortMission()
        audioMode = False
        curses.resetty()
        q.put('')

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
    writeScreen = curses.newwin(2, cols, rows - 3, 0)
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


def main(gru):
    global stdscr
    global activities
    stdscr = gru
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE),
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE),
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN),
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED),
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW),
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK),
    curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK),
    maybeTodo()
    activities = maybeActivities()
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    gui_thread = threading.Thread(target=gui)
    gui_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    wrapper(main)

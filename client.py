import socket, threading, queue
import curses
import random
import signal
import time
import os
import sys
import requests
#from desktop_notifier import DesktopNotifier, Urgency, Button
from todo import *
from datetime import datetime
from emojis import *
from radio import *
from activity import *
from nickname import randoum
from curses import wrapper

def handler(signum, frame):
    sys.exit(1)
    client.send("____deco".encode('utf-8'))
    curses.endwin()

 
signal.signal(signal.SIGINT, handler)
q = queue.Queue()
#notify = DesktopNotifier()

messages = []
users = 0
tabinfo = 0
activity = "chat"
letterColorIndex = 0
emojisNames = ["shrug", "wave", "raslefion", "nonmerci", "kill", "bizarre"]
radios = ["metal", "culture", "nolife", "u", "d", "stop"]
alecoute = "rien"
volume = 50
activities = {}

nickname = randoum()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((os.environ.get('FLOUNE_CHAT_SERVER', 'localhost'), int(os.environ.get('FLOUNE_CHAT_PORT', 5556))))


def receive():
    global users
    while True:
        try:
            message = client.recv(1024).decode('utf-8')

            if message == 'NICKNAME':
                client.send(nickname.encode('utf-8'))
            elif "NUMBEROFUSERS" in message:
                users = message.split("####")[1]
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
        if (len(m.split("::::")) > 1 and m.split("::::")[1] == "") or len(m) < 1:
            del(messages[i])
        elif "::::" in m:
            userMessage(m, i, win)
        elif "####" in m:
            systemMessage(m, i, win)

def userMessage(m, i, win):
    arr = m.split("::::")     
    if len(arr) > 1:
        colorIndex = (ord(arr[0][letterColorIndex]) % 5) + 1
        win.addstr(i + 3, 0, arr[0], curses.color_pair(colorIndex))
        win.refresh()
        win.addstr(i + 3, len(arr[0]) + 2, arr[1])
        win.refresh()

def systemMessage(m, i, win):
    arr = m.split("####")        
    if len(arr) > 1:
        colorIndex = 0
        win.addstr(i + 3, 0, arr[0], curses.color_pair(colorIndex))
        win.refresh()
        win.addstr(i + 3, len(arr[0]) + 2, arr[1])
        win.refresh()

def displayTodo(win):
    win.clear()
    win.refresh()
    win.addstr(0, 0, "TODO list", curses.color_pair(1))
    win.refresh()
    for i, todo in enumerate(todos):
        win.addstr(i + 2, 0, "{} - {}".format(i, todo["value"]), curses.color_pair(todo["color"]))
        win.refresh()

def displayTrack(win):
    i = 0
    win.clear()
    win.addstr(0, 0, "Tracker", curses.color_pair(1))
    win.refresh()
    keys_list = list(activities)
    for i, (k, v) in enumerate(activities.items()):
        if i > 0:
            key = keys_list[i]
            previousKey = keys_list[i - 1]
            duree = datetime.strptime(key, '%H:%M') - datetime.strptime(previousKey, '%H:%M')
            win.addstr(i + 2, 0, "{}".format(activities[previousKey]))
            win.refresh()
            win.addstr(i + 2, 20, "{}".format(duree))
            win.refresh()
        i+=1

def iterate(iterable):
    iterator = iter(iterable)
    item = iterator.next()

    for next_item in iterator:
        yield item, next_item
        item = next_item

    yield item, None



def updateGui(win):
    win.move(0, 0)
    win.clear()
    if activity == "chat":
        displayInfos(win)
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

    if c[1:] in emojisNames:
        emoj(nickname, c[1:], client)

    elif c[1:] in radios:
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
    win = curses.newwin(1, 100, 22, 0)
    win.keypad(True)
    curses.echo()
    win.clear()
    win.refresh()
    while True:
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

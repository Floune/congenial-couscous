import socket, threading, queue
import curses
import random
from nickname import randoum
from curses import wrapper
import signal
import time
import os
import sys
#from desktop_notifier import DesktopNotifier, Urgency, Button
import requests
import vlc
import json


def handler(signum, frame):
    sys.exit(1)
    client.send("____deco".encode('utf-8'))
    curses.endwin()

 
signal.signal(signal.SIGINT, handler)
q = queue.Queue()
#notify = DesktopNotifier()
p = vlc.MediaPlayer("https://listen.nolife-radio.com/stream")

volume = 50
messages = []
users = 0
alecoute = "rien"
tabinfo = 0
news = []
activity = "chat"
todos = []

letterColorIndex = 0

nickname = randoum()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((os.environ.get('FLOUNE_CHAT_SERVER', 'localhost'), int(os.environ.get('FLOUNE_CHAT_PORT', 5556))))

radios = {
  "metal": {
    "url": "http://radio.radiometal.com/radiometal.mp3",
    "commentaire": "metaaaal"
  },
  "nolife": {
    "url": "https://listen.nolife-radio.com/stream",
    "commentaire": "nolife mon gars"
  },
  "culture": {
    "url": "http://icecast.radiofrance.fr/franceculture-lofi.mp3",
    "commentaire": "la culture"
  },
}


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


def updateGui(win):
    win.move(0, 0)
    win.clear()
    if activity == "chat":
        displayInfos(win)
        displayMessages(win)
    elif activity == "todo":
        displayTodo(win)

def handleMessages(message):
    global messages
    if len(messages) > 16:
        del messages[0]
    messages.append(message)


def radioFrenezy(adresse, commentaire):
    global alecoute
    global p
    p.stop()
    p = vlc.MediaPlayer(adresse)
    p.audio_set_volume(volume)
    alecoute = commentaire
    p.play()

def handleCommand(c):
    global alecoute
    global p

    if c[1:] == "joke":
        jk = requests.get("https://api.chucknorris.io/jokes/random")
        client.send('{}::::{}'.format(nickname, jk.json()['value']).encode("utf8"))

    elif c[1:] == "shrug":
        client.send('{}::::{}'.format(nickname, "¯\\_(ツ)_/¯").encode("utf8"))

    elif c[1:] == "wave":
        client.send('{}::::{}'.format(nickname, "°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,").encode("utf8"))

    elif c[1:] == "raslefion":
        client.send('{}::::{}'.format(nickname, "(╯°□°）╯ ︵ ┻━┻").encode("utf8"))

    elif c[1:] == "nonmerci":
        client.send('{}::::{}'.format(nickname, "╭∩╮（︶︿︶）╭∩╮").encode("utf8"))

    elif c[1:] == "kill":
        client.send('{}::::{}'.format(nickname, "(╯°□°)--︻╦╤─ - - -").encode("utf8"))

    elif c[1:] == "bizarre":
        client.send('{}::::{}'.format(nickname, "(ノಠ益ಠ)ノ彡").encode("utf8"))

    elif c[1:] == "swagg":
        changeColor(letterColorIndex)

    elif c[1:] == "nolife":
        radioFrenezy(radios[c[1:]]["url"], radios[c[1:]]["commentaire"])

    elif c[1:] == "culture":
        radioFrenezy(radios[c[1:]]["url"], radios[c[1:]]["commentaire"])

    elif c[1:] == "metal":
        radioFrenezy(radios[c[1:]]["url"], radios[c[1:]]["commentaire"])

    elif c[1:] == "u":
        setVolume("up")

    elif c[1:] == "d":
        setVolume("down")

    elif c[1:] == "stop":
        alecoute = "plus rien"
        p.stop()

    elif c[1:] == "tab":
        handleTabs()

    elif c[1:] == "todo":
        changeActivity("todo")

    elif "new" in c[1:]:
        addTodo(c[1:])

    elif "done" in c[1:]:
        checkTodo(c[1:])

    elif "del" in c[1:]:
        delTodo(c[1:])

    elif c[1:] == "delall":
        delAllTodo()    

    elif c[1:] == "chat":
        changeActivity("chat")

    else:
        client.send('{}'.format(c).encode("utf8"))

    q.put("")

def handleTabs():
    global tabinfo
    tabinfo = tabinfo + 1 if tabinfo < 1 else 0

def addTodo(todo):
    global todos
    if len(todos) == 9:
        todos.append({"value": "finir mes autres todos", "color": 4})
    elif len(todos) < 10:
        todos.append({"value": todo[4:], "color": 4})
    syncTodos()

def checkTodo(cmd):
    global todos
    try:
        todos[int(cmd[5:6])]["color"] = 3
    except:
        print("MERDE")
    syncTodos()

def delTodo(cmd):
    global todos
    try:
        del(todos[int(cmd[4:5])])
    except:
        print("MERDE")
    syncTodos()

def delAllTodo():
    global todos
    todos = []
    syncTodos()

def syncTodos():
    global todos
    with open('excellentsystemededonnees.json', 'w') as outfile:
        json.dump(todos, outfile)

def changeActivity(newActivity):
    global activity
    activity = newActivity

def setVolume(comment):
    global volume
    if comment == "up":
        if volume < 90:
            volume += 10
    if comment == "down":
        if volume > 10:
            volume -= 10        
    p.audio_set_volume(volume)

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

def maybeTodo():
    global todos
    with open('excellentsystemededonnees.json') as json_file:
        data = json.load(json_file)
        for p in data:
            todos.append(p)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE),
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE),
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN),
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED),
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW),
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA),

    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK),


    maybeTodo()
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
    
    gui_thread = threading.Thread(target=gui)
    gui_thread.start()

wrapper(main)

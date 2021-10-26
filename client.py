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

letterColorIndex = 0

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

       
def displayInfos(win):
    win.move(0, 0)
    win.addstr(0, 0, "{} users |".format(users))
    win.refresh()
    win.addstr(0, 11, "Connecté en tant que ")
    win.refresh()
    win.addstr(0, 33, "{}".format(nickname), curses.color_pair(7))
    win.refresh()
    win.addstr(1, 0, "à l'écoute: {} | volume : {}%".format(alecoute, volume))
    win.refresh()


def displayMessages(win):
    for i, m in enumerate(messages):
        if "::::" in m:
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



def updateGui(win):
    win.move(0, 0)
    win.clear()
    displayInfos(win)
    displayMessages(win)

def handleMessages(message):
    global colorSequence
    global messages
    if len(messages) > 16:
        del messages[0]
    messages.append(message)

def handleCommand(c):
    global alecoute
    global p
    if c[1:] == "joke":
        jk = requests.get("https://api.chucknorris.io/jokes/random")
        client.send('{}::::{}'.format(nickname, jk.json()['value']).encode("utf8"))

    elif c[1:] == "shrug":
        client.send('{}::::{}'.format(nickname, "¯\\_(ツ)_/¯").encode("utf8"))

    elif c[1:] == "nolife":
        p.stop()
        p = vlc.MediaPlayer("https://listen.nolife-radio.com/stream")
        p.audio_set_volume(volume)
        alecoute = "nolife radio mon gars"
        p.play()

    elif c[1:] == "culture":
        p.stop()
        p = vlc.MediaPlayer("http://icecast.radiofrance.fr/franceculture-lofi.mp3")
        p.audio_set_volume(volume)
        alecoute = "la culture"
        p.play()

    elif c[1:] == "metal":
        p.stop()
        p = vlc.MediaPlayer("http://radio.radiometal.com/radiometal.mp3")
        p.audio_set_volume(volume)
        alecoute = "la culture"
        p.play()


    elif c[1:] == "u":
        setVolume("up")

    elif c[1:] == "d":
        setVolume("down")

    elif c[1:] == "stop":
        alecoute = "plus rien"
        p.stop()

    elif c[1:] == "swagg":
        changeColor(letterColorIndex)

    else:
        client.send('{}'.format(c).encode("utf8"))


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
    win = curses.newwin(1, 200, 22, 0)
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
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE),
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE),
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN),
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED),
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW),
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_MAGENTA),

    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK),

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()
    
    gui_thread = threading.Thread(target=gui)
    gui_thread.start()

wrapper(main)

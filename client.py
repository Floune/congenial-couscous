import socket, threading
import curses
import random
from nickname import randoum
from curses import wrapper
import signal
import time
 
def handler(signum, frame):
    curses.endwin()
    exit(1)
 
signal.signal(signal.SIGINT, handler)


messages = []
history = []
currentMsg = ""
colors = []
colorSequence = []

nickname = randoum()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8767))



def receive(guiwin):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                handleMessages(message)
                updateGui(guiwin)

        except:
            print("An error occured!")
            client.close()
            break

        
def gui():
    win = curses.newwin(21, 200, 0, 0)
    win.clear()
    win.refresh()
    return win

       
def updateGui(win):
    win.move(0, 0)
    win.clear()
    win.refresh()

    for i, m in enumerate(messages):
        arr = m.split(":::b'")
        if len(arr) > 1:
            win.addstr(i, 0, arr[0], curses.color_pair(colorSequence[i]))
            win.addstr(i, len(arr[0]) + 2, arr[1][:-1])
    win.refresh()

def handleMessages(message):
    global colorSequence
    if len(messages) > 20:
        del messages[0]
        del colorSequence[0]
    colorSequence.append(random.choice(range(1, 5)))
    messages.append(message)



def write():
    win = curses.newwin(1, 200, 23, 0)
    win.clear()
    win.refresh()
    win.keypad(True)
    curses.echo()
    while True:
        win.move(0, 0)
        c = win.getstr(0, 0)
        message = '{}:::{}'.format(nickname, c)
        client.send(message.encode('ascii'))
        win.clear()
        win.refresh()


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE),
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE),
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN),
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED),
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_YELLOW),
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_MAGENTA),
    

    g = gui()

    receive_thread = threading.Thread(target=receive, args=(g,))
    receive_thread.start()
    write_thread = threading.Thread(target=write)
    write_thread.start()
    # hacker_thread = threading.Thread(target=hack)
    # hacker_thread.start()

wrapper(main)
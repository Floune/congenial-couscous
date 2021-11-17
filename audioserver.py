#!/usr/bin/python3

import socket
import threading

ip = ""
port = 8768
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
connections = []



def accept_connections():
    s.listen(100)

    print('Running on IP: '+ip)
    print('Running on port: '+str(port))
    
    while True:
        c, addr = s.accept()
        connections.append(c)

        threading.Thread(target=handle_client,args=(c,addr,)).start()
    
def broadcast(sock, data):
    for client in connections:
        if client != s and client != sock:
            try:
                client.send(data)
            except:
                terminate(c)


def handle_client(c,addr):
    while 1:
        try:
            data = c.recv(1024)
            broadcast(c, data)
        
        except:
            terminate(c)
            break

def terminate(c):
    print(len(connections))
    c.close()
    connections.remove(c)
    print(len(connections))


accept_connections()

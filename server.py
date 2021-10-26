import socket, threading
import sys
import signal
host = ''                                                    
port = 8767                                                       
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             
server.bind((host, port))                                             
server.listen()
 
def handler(signum, frame):
    sys.exit(1)
 
signal.signal(signal.SIGINT, handler)


clients = []
nicknames = []

def broadcast(message): 
    for client in clients:
        client.send(message)

def handle(client):                                         
    while True:
        try:        
            message = client.recv(1024)
            print(message)
            if message.decode('utf-8') == "____deco":
                sys.exit()
                deco(client)
            elif message.decode('utf-8')[0] == "/":
                handleCommand(message.decode('utf-8')[1:], client)
            else:
                broadcast(message)
        except:   

            deco(client)
            break

#Connection
def connect():  
    while True:
        client, address = server.accept()     
        
        #demande de pseudo
        client.send('NICKNAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print("{} connected as {}".format(str(address), nickname))
        broadcast("{}::::joined!".format(nickname).encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def deco(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast('{}::::left!'.format(nickname).encode('utf-8'))
    print('{} left!'.format(nickname).encode('utf-8'))
    nicknames.remove(nickname)

def handleCommand(c, client):
    if (c == "help"):
        client.send('system::::/joke /shrug /nolife /stop'.encode('utf-8'))
    else:
        client.send('system:::: /help pour la liste des commandes'.encode('utf-8'))

connect()


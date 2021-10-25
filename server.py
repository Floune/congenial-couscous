import socket, threading
import sys
host = ''                                                    
port = 8767                                                           
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             
server.bind((host, port))                                             
server.listen()


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
            if message.decode('ascii') == "____deco":
                sys.exit()
                deco(client)
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
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("{} connected as {}".format(str(address), nickname))
        broadcast("{}::::joined!".format(nickname).encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def deco(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast('{}::::left!'.format(nickname).encode('ascii'))
    print('{} left!'.format(nickname).encode('ascii'))
    nicknames.remove(nickname)

connect()
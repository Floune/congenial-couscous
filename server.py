import socket, threading
host = '127.0.0.1'                                                    
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
            broadcast(message)
        except:        
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{}:::b\'left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():  
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{}:::b'joined!".format(nickname).encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
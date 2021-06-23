from socket import *
from select import *
from threading import *

HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)
users = []
serverSocket = socket(AF_INET, SOCK_STREAM)

class Waiting(Thread):
    global serverSocket
    global ADDR
    
    def __init__(self):
        super().__init__()
        serverSocket.bind(ADDR)
        serverSocket.listen(100)
        
    def run(self):
        try:
            while True:
                clientSocket, addr = serverSocket.accept()
                if not clientSocket:
                    continue
                t2 = RaspberryServer(clientSocket)
                t2.start()
        except:
            pass

class RaspberryServer(Thread):
    global ADDR
    global users
    global serverSocket
    
    def __init__(self, socket):
        super().__init__()
        users.append(socket)
        self.socket = socket

    def run(self):
        print("sub thread start", len(users))
        print('Connected by', ADDR)
        print('client Socket', self.socket)
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print('Received from', ADDR, data.decode())
                t3 = ServerSender(data)
                t3.start()
        finally:
            users.remove(self.socket)
            self.socket.close()
            serverSocket.close()
            
class ServerSender(Thread):
    global users
    
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        for i in range(len(users)):
            tempSocket = users[i]
            tempSocket.sendall(self.data)
            
t1 = Waiting()
t1.start()

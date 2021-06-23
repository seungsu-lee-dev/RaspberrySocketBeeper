from socket import *
from select import *
from threading import *

HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)
users = []
serverSocket = socket(AF_INET, SOCK_STREAM)
usersNickname = []

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
    global usersNickname
    
    def __init__(self, socket):
        super().__init__()
        users.append(socket)
        self.socket = socket

    def nickname(self):
        try:
            while True:
                nickname = self.socket.recv(1024)
                if "nickname:" in nickname.decode():
                    nickname = nickname.decode().split(":")[1]
                    usersNickname.append(nickname)
                    self.socket.sendall("Entered ChatRoom".encode())
                    break
        except:
            pass
                    

    def run(self):
        self.nickname()
        print("sub thread start", len(users))
        print('Connected by', ADDR)
        print('client Socket', self.socket)
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print('Received from', ADDR, data.decode())
                senderSocketIndex = users.index(self.socket)
                t3 = ServerSender(data, senderSocketIndex)
                t3.start()
        finally:
            users.remove(self.socket)
            del usersNickname[senderSocketIndex]
            self.socket.close()
            serverSocket.close()
            
class ServerSender(Thread):
    global users
    
    def __init__(self, data, senderSocketIndex):
        super().__init__()
        self.data = data
        self.senderSocketIndex = senderSocketIndex

    def run(self):
        for i in range(len(users)):
            tempSocket = users[i]
            newData = usersNickname[self.senderSocketIndex]+" : "+self.data.decode()
            tempSocket.sendall(newData.encode())
            
t1 = Waiting()
t1.start()

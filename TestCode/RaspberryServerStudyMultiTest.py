from socket import *
from select import *
from threading import *

HOST = '220.69.249.233'
PORT = 9999
ADDR = (HOST, PORT)
users = []
serverSocket = socket(AF_INET, SOCK_STREAM)
##serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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
##                print('Connected by', ADDR)
##                print('clientSocket', clientSocket)
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
                self.socket.sendall(data)
        finally:
            self.socket.close()
            serverSocket.close()
t1 = Waiting()
t1.start()

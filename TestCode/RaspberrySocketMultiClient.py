from socket import *
import sys
from threading import *

class ClientInit:
    HOST = 'localhost'
    PORT = 9999
    ADDR = (HOST, PORT)

    def __init__(self, nickname):
        super().__init__()
        self.clientSocket = None
        self.nickname = nickname
        
    def conn(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        try:
            self.clientSocket.connect(ClientInit.ADDR)
        except Exception as e:
            print("clientInit")
            print('%s:%s' % ClientInit.ADDR)
            print(e)
            sys.exit()
        
    def run(self):
        self.conn()
        t1 = NickName(self.nickname, self.clientSocket)
        t1.start()
        
class NickName(Thread):

    def __init__(self, nickname, socket):
        super().__init__()
        self.clientSocket = socket
        self.nickname = nickname

    def run(self):
        nickname = "nickname:" + self.nickname
        self.clientSocket.sendall(nickname.encode())
        data = self.clientSocket.recv(1024)
        if "Entered ChatRoom" in data.decode():
            print("Entered ChatRoom")
            t2 = ClientSender(self.clientSocket)
            t2.start()
            t3 = ClientReceiver(self.clientSocket)
            t3.start()
            
class ClientSender(Thread):
    
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
        
    def run(self):

        while True:
            sendData = input()
            if sendData:
                self.clientSocket.sendall(sendData.encode())
                if sendData == '\stop':
                    break
        print("ClientSenderThread Stop")

class ClientReceiver(Thread):
    
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
        
    def run(self):
        while True:
            data = self.clientSocket.recv(1024)
            if data:
                print(repr(data.decode())[1:-1])
                if data == '\stop':
                    break
        self.clientSocket.close()
        print("ClientReceiverThread Stop")

nickname = input("input nickname: ")
c = ClientInit(nickname)
c.run()

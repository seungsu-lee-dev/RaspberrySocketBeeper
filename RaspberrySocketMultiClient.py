from socket import *
import sys
from threading import *

class ClientInit:
    global clientSocket
    HOST = 'localhost'
    PORT = 9999
    ADDR = (HOST, PORT)

    def __init__(self):
        super().__init__()
        self.clientSocket = None
        
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
        t1 = ClientSender(self.clientSocket)
        t1.start()
        t2 = ClientReceiver(self.clientSocket)
        t2.start()

class ClientSender(Thread):
    
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
        
    def run(self):
        while True:
            sendData = input("input data: ")
            if sendData:
                print('Send')
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
                # 안되면 sender bool 수정
                print('Received', repr(data.decode()))
                if data == '\stop':
                    break
        self.clientSocket.close()
        print("ClientReceiverThread Stop")

c = ClientInit()
c.run()

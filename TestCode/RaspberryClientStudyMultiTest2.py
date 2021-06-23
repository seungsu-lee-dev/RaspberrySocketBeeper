from socket import *
import sys
from threading import *

# socket
##clientSocket = socket(AF_INET, SOCK_STREAM)

class ClientSender(Thread):
##    global clientSocket
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
    def run(self):
        while True:
##            try:
            sendData = input("input data: ")
            if sendData:
                print('Send')
                self.clientSocket.sendall(sendData.encode())
                if sendData == '\stop':
                    break
        print("ClientSenderThread Stop")
##            except Exception as e:
##                print("senderError")
##                print(e)
##                break

class ClientReceiver(Thread):
##    global clientSocket
    def __init__(self, socket):
        super().__init__()
        self.clientSocket = socket
        
    def run(self):
        while True:
##            try:
            data = self.clientSocket.recv(1024)
            if data:
                # 안되면 sender bool 수정
                print('Received', repr(data.decode()))
                if data == '\stop':
                    break
        self.clientSocket.close()
        print("ClientReceiverThread Stop")
                    
##            except Exception as e:
##                print("receiverError")
##                print(e)
##                clientSocket.close()
##                break

class ClientInit:
    global clientSocket
    HOST = '220.69.249.233'
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


c = ClientInit()
c.run()

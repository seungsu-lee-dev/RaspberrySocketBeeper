from socket import *
import sys
from threading import *

HOST = '220.69.249.233'
##HOST = '192.168.0.85'
##HOST = 'localhost'
PORT = 9999
ADDR = (HOST, PORT)

# socket
clientSocket = socket(AF_INET, SOCK_STREAM)

# connect
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print('%s:%s' % ADDR)
    sys.exit()

class ClientSender(Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        data = clientSocket.recv(1024)
        if data:
            print('Received', repr(data.decode()))

t1 = ClientSender()
t1.start()

# send/recv
try:
    while True:
##        clientSocket.sendall('안녕'. encode())
        sendData = input("input data: ")
        clientSocket.sendall(sendData.encode())

# close
finally:
    clientSocket.close()

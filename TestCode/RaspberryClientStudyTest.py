from socket import *
import sys

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

# send/recv
try:
    while True:
##        clientSocket.sendall('안녕'. encode())
        sendData = input("input data: ")
        clientSocket.sendall(sendData.encode())
        data = clientSocket.recv(1024)
        if data:
            print('Received', repr(data.decode()))

# close
finally:
    clientSocket.close()

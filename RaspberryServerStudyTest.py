from socket import *
from select import *

HOST = 'localhost'
PORT = 9999
##users = []
##serverSocket = []

##print(HOST)

# socket
serverSocket  = socket(AF_INET, SOCK_STREAM)
##serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# bind
serverSocket.bind((HOST, PORT))

# listen
serverSocket.listen()

# accept
clientSocket, addr = serverSocket.accept()

# send /receive
print('Connected by', addr)
print('client Socket', clientSocket)
print(HOST)

try:
    while True:
        data = clientSocket.recv(1024)
        if not data:
            break
        print('Received from', addr, data.decode())
        clientSocket.sendall(data)
finally:
    clientSocket.close()
    serverSocket.close()
    
# close

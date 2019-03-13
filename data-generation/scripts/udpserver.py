#!/usr/local/bin/python
import random
from socket import *
import sys
serverSocket = socket(AF_INET, SOCK_DGRAM)
print('connecting to localhost port 5005', file=sys.stderr)
serverSocket.bind(('', 5005))
print('listening on localhost port 5005', file=sys.stderr)

while True:
    rand = random.randint(0, 10)
    print('waiting for a connection', file=sys.stderr)
    message, address = serverSocket.recvfrom(1024)
    print('Recieved" %s from %s' %(message,address))
    message = message.upper()
    if rand >= 0:
        serverSocket.sendto(message, address) 
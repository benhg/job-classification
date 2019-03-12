#!/usr/local/bin/python
import random
from socket import *
import sys
serverSocket = socket(AF_INET, SOCK_DGRAM)
print >>sys.stderr, 'connecting to localhost port 5005'
serverSocket.bind(('', 5005))
print >>sys.stderr, 'listening on localhost port 5005'

while True:
    rand = random.randint(0, 10)
    print >>sys.stderr, 'waiting for a connection'
    message, address = serverSocket.recvfrom(1024)
    print 'Recieved" %s from %s' %(message,address)
    message = message.upper()
    if rand >= 0:
        serverSocket.sendto(message, address) 
#!/usr/local/bin/python
#USAGE: ./udpclient.py <INT datagrams> <STRING message>
import time
from socket import *
import sys

failed=0
passed=0
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(.1)
message = sys.argv[2]
addr = ("127.0.0.1", 5005)
start = time.time()
for pings in range(0,int(sys.argv[1])):
    print 'Sending %s %d' % (message, pings)
    clientSocket.sendto(message, addr)
    try:
        data, server = clientSocket.recvfrom(1024)
        print 'Recieved %s %d' % (data, pings)
        passed+=1
    except timeout:
        print 'FAILED'
        failed+=1
end = time.time()
elapsed = end - start
pings+=1
fail=float(float(failed)/float(pings))
succ=float(float(passed)/float(pings))
print "%d datagrams recieved out of %s attempted (%s success rate, %s fail rate)" % (passed,pings,succ,fail)
print "%d datagrams took %s seconds" % (pings,elapsed)
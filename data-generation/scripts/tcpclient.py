#!/usr/local/bin/python
#USAGE: ./tcpclient.py <INT segments> <STRING message>

import socket
import sys
import time

passed=0
failed=0
pings=0



start=time.time()
for i in range(0,int(sys.argv[1])):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5005)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)
    try:
        
        # Send data
        message = sys.argv[2]
        print >>sys.stderr, 'sending "%s"' % message
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        packets=0
        while amount_received < amount_expected:
            data = sock.recv(32)
            amount_received += len(data)
            packets+=1
            pings += 1
            print >>sys.stderr, 'received "%s"' % data
            passed+=1
        #else:
         #   failed+=1

    finally:
        #print >>sys.stderr, 'received %s packets' % packets
        #print >>sys.stderr, 'received %s bytes' % len(data)
        print >>sys.stderr, 'closing socket'
        sock.close()
end = time.time()
elapsed = end - start
fail=float(float(failed)/float(pings))
succ=float(float(passed)/float(pings))
print "%d segments recieved out of %s attempted (%s success rate, %s fail rate)" % (passed,pings,succ,fail)
print "%d segments took %s seconds" % (pings,elapsed)


#!/usr/local/bin/python
#USAGE: ./rudpclient.py <INT datagrams> <STRING message>

from rudpDumbUser import *
from sys import argv
import time

failed=0
passed=0
pings=0
print('--------------------- Start of Test (Client)----------------------')
print('Connected to port 5005')
start = time.time()
for i in range(0,int(argv[1])):	
	c = rudpDumbSender(50020)
	dataSize = 10000
	data = argv[2]
	print('==> [Data-Delivery] Sender - Sending')
	c.sendData(data)
	c.skt.close()

	pings+=1

end = time.time()
elapsed = end - start
fail=float(float(failed)/float(pings))
succ=float(float(passed)/float(pings))
print("sent %d datagrams" % pings)
print("%d datagrams took %s seconds" % (pings,elapsed))
print('--------------------- End of Test (Client)----------------------')

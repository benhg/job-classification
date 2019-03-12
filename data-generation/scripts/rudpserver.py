#!/usr/local/bin/python
from rudpDumbUser import *
from sys import *
packets=0
print '-------------------------Testing (Dumb Receiver)---------------------\n'
print "Connecting to port 5005"
r = rudpDumbReceiver(SERVER_PORT)
print '==> Receiver is running.\n'
while True:
	data = r.receive()
	if data: 	
		stdout.write("Recieved: "+data+'\n')
		packets+=1
		print packets
	else:		
		stdout.write('x \n')
	stdout.flush()


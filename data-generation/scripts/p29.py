list=[]
for a in range(2,101,1):
	for b in range(2,101,1):
		list.append(int(a**b))
list=set(list)
print len(list)
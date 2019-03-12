values=[1,2,5,10,20,50,100,200]
we_want=200
ways=[]
ways.append(1)
for value in range(0,len(values),1):
	for j in range(values[value],we_want,1):
		ways[j]+= ways[j-values[value]] 
print len(ways)
print ways
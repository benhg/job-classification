import time as t

def factors(n):    
    return reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))



def primesBelow(n):
	time=t.time()
	list=[]
	for i in range(1,n,1):
		if len(factors(i))==2:
			list.append(i)
	timenow=t.time()-time
	print(timenow)
	return list

#print(primesBelow(400000))
ti=t.time()
print(factors(235958091582))
print (t.time()-ti)

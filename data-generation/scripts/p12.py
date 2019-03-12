def factors(n):    
    return reduce(list.__add__, 
                ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))


def triangular(n):
    return sum(range(n+1))
print(triangular(9))
print(factors(triangular(9)))
print len(factors(triangular(9)))
for i in range(1,500000,1):
	print(i)
	print(triangular(i))
	print(len(factors(triangular(i))))
	print(factors(triangular(i)))
	if len(factors(triangular(i))) > 500:
    	    print(triangular(i))


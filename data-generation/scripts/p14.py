def collatz(x):
    seq = [x]
    if x < 1:
       return []
    while x > 1:
       if x % 2 == 0:
         x = x / 2
       else:
         x = 3 * x + 1 
       seq.append(x)
    return seq
collatz1=[]
for i in range(1000000):
	j=collatz(i)
	print i
	if len(j)>len(collatz1):
		collatz1=j
print(collatz1)


def palind(n):
	return str(n) == str(n)[::-1]

currentLarge=0
for i in range(100,999,1):
	for j in range(100,999,1):
		k=i*j
		if(palind(k)==True) and (k>=currentLarge):
			currentLarge=k
print(currentLarge)
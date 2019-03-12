j=0
for i in range(2,335000,1):
	sum=0
	number=i
	while(number>0):
		d=number%10
		number /= 10
		temp=d
		for k in range(1,5,1):
			temp*=d
		sum+=temp
	if sum == i:
		j +=i

print j
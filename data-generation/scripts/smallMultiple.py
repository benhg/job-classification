list=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

def divisibleBy(n,k):
		if n % k == 0 and k==1:
			return True
		elif n%k==0 and k>1:
			return True and divisibleBy(n,k-1)
		else:
			return False
def tester():
	for i in range(0,10000000000,20):
		if i !=0:	
			if divisibleBy(i,20):
				return i

final=tester()
print(final)
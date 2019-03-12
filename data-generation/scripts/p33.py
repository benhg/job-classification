from fractions import gcd
list=[]
"""
There are 4 ways this could work.  (10i+n/10i+d)=(n/d)
2. (10n+i/10d+i)=n/d 3. 10i+n/10d+i=n/d
4. 10n+i/10i+d=n/d

all solutons will have the form 10n+i/10i+d
"""
numproduct=1
denomproduct=1


for i in range(1,9,1):
	den=1
	while den<i:
		num=1
		while num<den:
			if (((num*10)+i)*den)==(num*((i*10)+den)):
				denomproduct*=den
				numproduct*=num
			num+=1
		den+=1


denomproduct/=(gcd(numproduct,denomproduct))
print denomproduct*numproduct
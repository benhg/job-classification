


def fibRecur(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return fib(n-1)+fib(n-2)

def fib(n):
    a, b = 0, 1
    for i in range(0, n):
        a, b = b, a + b
    return a


final=0
for i in range(0,50,1):
	x=fib(i)
	print(x)
	print(i)
	if x<4000000 and x%2==0:
		final+=x
print(final)
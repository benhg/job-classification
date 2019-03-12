def fib(n):
    a, b = 0, 1
    for i in range(0, n):
        a, b = b, a + b
    return a
for i in range(19999):
	if len(str(fib(i)))>=1000:
		print i
		print fib(i)
		break
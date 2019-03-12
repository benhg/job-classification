from math import factorial

def factorial1(n):return reduce(lambda x,y:x*y,[1]+range(1,n+1))

strin=[int(char) for char in str((factorial(100)))]
print(sum(strin))

import math
def Divisorsbaritself(x):
    divList = [1]
    y = 2
    while y <= math.sqrt(x):
        if x % y == 0:
            divList.append(y)
            divList.append(int(x / y))
        y += 1
    return sum(divList)

def amicable(n):
    solution = [i for i in xrange(n) if Divisorsbaritself(i)!=i and Divisorsbaritself(Divisorsbaritself(i)) == i]
    return sum(solution)
print amicable(10000)
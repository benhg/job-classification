def pythagore_triplets(n):
    maxn=int(n*(2**0.5))+1 # max int whose square may be the sum of two squares
    squares=[x*x for x in xrange(maxn+1)] # calculate all the squares once
    reverse_squares=dict([(squares[i],i) for i in xrange(maxn+1)]) # x*x=>x
    for x in xrange(1,n):
        x2 = squares[x]
        for y in xrange(x,n+1):
            y2 = squares[y]
            z = reverse_squares.get(x2+y2)
            if z != None:
                print(x)
                print(y)
                print(z)
                if x + y + z == 1000:
                   print(x)
                   print(y)
                   print(z)

pythagore_triplets(100000)
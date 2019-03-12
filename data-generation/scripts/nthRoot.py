def rtn (y,k):
    x=y**(1/k)
    if x>=0:
        x=int(x+0.5)
        return x 
    else:
        x=int(x-0.5)
        return x


print(rtn(25,2))
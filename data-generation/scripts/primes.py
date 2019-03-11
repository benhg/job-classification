print("ENTERING PROBLEM 4")
_ = input("Press any key when ready to continue")
find = False
primes = [2]
print(2)
for i in range(3, 10001):
    for prime in primes:
        if (i % prime == 0):
            find = True
            continue
        if (prime > sqrt(i)):
            continue
    if find == True:
        find = False
        continue
    primes.append(i)
    print(i)
print("EXITING PROBLEM 4")
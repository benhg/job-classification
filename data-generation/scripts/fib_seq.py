# ============ PROBLEM 1 ============
print("ENTERING P. 1: Fibonacci Sequence")
_ = input("Press any key when ready to continue")


def fibs_below(n):
    f1 = 0
    f2 = 1

    if (n < 1):
        return
    for x in range(0, n):
        if(f2 <= n):
            print(f2, end=" ")
            next = f1 + f2
            f1 = f2
            f2 = next
        else:
            break
    print()


fibs_below(int(input("Enter n for fibonnaci sequence:")))

print("EXITING P.1")
# ============ END PROBLEM 1 ============
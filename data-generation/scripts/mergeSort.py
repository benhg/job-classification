import random


def mergeSort(x):
    sorted = []

    #Base case. If length is 1, return the (sorted) singleton
    if len(x) < 2:
        return x

    #Find the middle value. This favors the left (bottom) if length is even
    mid = int(len(x)/2)

    #recursive step. call mergeSort on each half-list
    y = mergeSort(x[:mid])
    z = mergeSort(x[mid:])
    i = 0
    j = 0
    #merge the arrays back together
    while i < len(y) and j < len(z):
            if y[i] > z[j]:
                sorted.append(z[j])
                j += 1
            else:
                sorted.append(y[i])
                i += 1
    sorted += y[i:]
    sorted += z[j:]
    return sorted

def testSort(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))


  
for index, val in enumerate(range(0,1000000,100)):
    testArray=[random.randint(-10000000,10000000) for r in range(val)]
    print("Test Number %s. Length:%s"%(index, val))
    #print testArray
    #print testSort(testArray)
    result=mergeSort(testArray)
    #print result
    print("Sort Worked?: %s"%(testSort(result)))

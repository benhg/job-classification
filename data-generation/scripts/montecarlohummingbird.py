#!/usr/bin/python

import math
import random
import time
import multiprocessing


def random_three_vector():
    phi = random.uniform(0,math.pi*2)
    costheta = random.uniform(-1,1)
    theta = math.acos( costheta )

    x = math.sin( theta) * math.cos( phi )
    y = math.sin( theta) * math.sin( phi )
    z = math.cos( theta )
    return [x,y,z]


def monteCarlo():
    #initialize variables
    outfile=open("out.txt",'a')
    logfile=open('log.txt','a')
    numTries=1000000
    startTime=time.time()
    numSuccesses=0

    #randomly test 1 million times and see what happens
    for j in range(0,numTries,1):
        #vector representing distance of 0 from origin
        birdPosition=[0.0,0.0,0.0]
        for i in range(0,numJumps,1):
            #generate a random vector
            lenJump=random_three_vector()
            #add to x and y components of bird position vectors
            birdPosition[0]+=lenJump[0]
            birdPosition[1]+=lenJump[1]
            birdPosition[2]+=lenJump[2]
        #compute magnitude of final bird position vector
        birdMagnitude=((birdPosition[0]**2+birdPosition[1]**2)**0.5)

        #check if bird landed where we wanted it to
        if birdMagnitude<=1.0:
            #keep track of successes
            numSuccesses+=float(1)
    
    #compute success rate
    successRate=float(numSuccesses/numTries)
    
    endTime=time.time()
    elapsed=endTime-startTime

    print "If the bird jumps %s times, it will land in the original circle  approximately %s times, representing a success rate of %s"%(numJumps,int(numSuccesses),successRate)
    outfile.write("If the bird jumps %s times, it will land in the original circle  approximately %s times, representing a success rate of %s\n"%(numJumps,int(numSuccesses),successRate))
    print "%s trials of %s jumps took %s seconds"%(numTries,numJumps,elapsed)
    logfile.write("%s trials of %s jumps took %s seconds"%(numTries,numJumps,elapsed))
    outfile.close()
    logfile.close()


#multithreading. This problem will take over the entire computer if allowed.
if __name__ == '__main__':
    maxNumJumps=50
    jobs = []
    for numJumps in range(0,maxNumJumps,1):
        p = multiprocessing.Process(target=monteCarlo)
        jobs.append(p)
        p.start()
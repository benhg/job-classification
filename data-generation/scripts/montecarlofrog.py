#!/usr/bin/python

import math
import random
import time
import multiprocessing


def monteCarlo():
    # initialize variables
    outfile = open("out.txt", 'a')
    logfile = open('log.txt', 'a')
    numTries = 1000000
    lenJump = 1
    startTime = time.time()
    numSuccesses = 0

    # randomly test 1 million times and see what happens
    for j in range(0, numTries, 1):
        # vector representing distance of 0 from origin
        frogPosition = [0.0, 0.0]
        for i in range(0, numJumps, 1):
            # generate a random angle
            theta = random.uniform(0, 2 * math.pi)
            # add to x and y components of frog position vectors
            frogPosition[0] += lenJump * math.cos(theta)
            frogPosition[1] += lenJump * math.sin(theta)
        # compute magnitude of final frog position vector
        frogMagnitude = ((frogPosition[0]**2 + frogPosition[1]**2)**0.5)

        # check if frog landed where we wanted it to
        if frogMagnitude <= 1.0:
            # keep track of successes
            numSuccesses += float(1)

    # compute success rate
    successRate = float(numSuccesses / numTries)

    endTime = time.time()
    elapsed = endTime - startTime

    print(
        "If the frog jumps %s times, it will land in the original circle  approximately %s times, representing a success rate of %s" %
        (numJumps, int(numSuccesses), successRate))
    outfile.write(
        "If the frog jumps %s times, it will land in the original circle  approximately %s times, representing a success rate of %s\n" %
        (numJumps, int(numSuccesses), successRate))
    print(
        "%s trials of %s jumps took %s seconds" %
        (numTries, numJumps, elapsed))
    logfile.write(
        "%s trials of %s jumps took %s seconds" %
        (numTries, numJumps, elapsed))
    outfile.close()
    logfile.close()


# multithreading. This problem will take over the entire computer if allowed.
if __name__ == '__main__':
    maxNumJumps = 50
    jobs = []
    for numJumps in range(0, maxNumJumps, 1):
        p = multiprocessing.Process(target=monteCarlo)
        jobs.append(p)
        p.start()

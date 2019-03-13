import time

with open('list.txt.txt') as f:
        for line in f:
                print("Working. . .")
                time.sleep(.25)
                print(line)
                time.sleep(.25)
                print("Loading Next. . .")
print("Done Hacking")
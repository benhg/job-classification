import pandas as pd, math as math, sys as sys
from time import sleep

#Defines locations and people
filepath=input("Where is the file located?")
person=input("Who is the candidate this data is for?")

#parses data
file=pd.read_csv(filepath)

#gets sample size
n=len(file)

#tabulates yesses
#sleep statements are for debugging purposes and will be removed
yes=0

yes+=1 if i[2] == "Yes" for i in file
for i in file:
	print i
	sleep(5)
	print i[0]
	sleep(5)
	print i[1]
	sleep(5)
	print i[2] if i[2] is not None
	if str(i[1])=="Yes":
		yes+=1

#finds number of noes, defined by the fact that no plus yes equals total responses
no=n-yes

#checks for comp-sci and data entry caused impossibility
if yes is 0 or yes is None or no is 0 or no is None or n is 0 or n is None:
	print "Something Fucked Up"
	sys.exit(1)

#calculates necessary values for confidence interval (that have not been found yet)
zScore=2.327
p=float(yes/total)
q=float(no/total)

#calculates confidence interval
MOE=zScore*(math.sqrt((p*q)/n))
bottom=p-MOE
top=p+MOE

#prints information in human-readable, contextualized form
print "With 99 per cent certainty, the proportion of voters likely to vote for %s is between %s and %s. Expected proportion: %s; Margin of Error: %s" % (person, bottom,top,p,MOE)
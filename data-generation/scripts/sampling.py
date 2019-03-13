import pandas as pd
import random as rdm

framelist=[]
frame_2019_15=pd.read_csv("2019_15.csv")
frame_2017_15=pd.read_csv("2017_15.csv")
frame_2018_15=pd.read_csv("2018_15.csv")
framelist.append(frame_2019_15)
framelist.append(frame_2018_15)
framelist.append(frame_2017_15)

sampleFrameMale=[]
sampleFrameFemale=[]
for frame in framelist:
	males=[]
	females=[]
	while len(males)<10 or len(females)<10:
		randomIndex=rdm.choice(range(0,len(frame),1))
		print(frame["Gender"][randomIndex])
		if (not pd.isnull(frame["Mile"][randomIndex])) and frame["Mile"][randomIndex] is not "DNR" and frame["Mile"][randomIndex] is not "Rx":	
			if frame["Gender"][randomIndex] == "M":
				print(len(males))
				if len(males)<10:
					males.append(frame["Mile"][randomIndex])
			if frame["Gender"][randomIndex] == "F":
				if len(females)<10:
					females.append(frame["Mile"][randomIndex])
	sampleFrameFemale.append(females)
	sampleFrameMale.append(males)
file=open("sampleframe2015_male.txt","w")
file.write(str(sampleFrameMale))
file2=open("sampleframe2015_female.txt","w")
file2.write(str(sampleFrameFemale))

print(sampleFrameMale)
print(sampleFrameFemale)
import json
import pickle

index_int=0

picklefile=open('mapping.pkl')

with open("wos.net","rt") as fh:
	line=fh.readline()
	while line:
		line=fh.readline()
		line=line.split(" ")
		if line[0] !="*verticies":
			if index_int<=line[0]:
				pickle.dump({"int_id":line[0],"wos_id":line[1]})
				index_int+=1
			else:
				break


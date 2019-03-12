+from genderizer.genderizer import Genderizer as g

names=open('genders_2.txt')
nones=open('nones.txt','w')
nones1=[]
for name in names:
	firstandLastname=name.split("|")[2]
	firstname=firstandLastname.split(' ')[0]
	print firstname
	gender=name.split("|")[3]
	print gender
	if gender is None or "None" in gender:
		nones1.append(firstandLastname)
print nones1
nones.write(str(nones1))
print len(nones1)

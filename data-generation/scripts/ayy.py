def inches_feetinches(n):
	feet=int(n/12)
	inches=n%12
	return("%s Feet, %s Inches")%(feet,inches)
print(inches_feetinches(82))
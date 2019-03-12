sumsquare=0
for i in range(0,101,1):
	sumsquare+=i
sumsquare=sumsquare**2

squaresum=0
for j in range(0,101,1):
	squaresum+=(j**2)

print((sumsquare-squaresum))
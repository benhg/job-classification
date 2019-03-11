# ============ PROBLEM 2 ============
print("ENTERING P. 2 (2.9): Madelung Constant")
_ = input("Press any key when ready to continue")
print("This version is really slow because it grows in O(n^3), so I only set L to 10")

M = 0
L = 10
for i in range(-L, L+1):
    for j in range(-L, L+1):
        for k in range(-L, L+1):
            if not(i == j == k == 0):

                M += ((-1)**(i+j+k))/((i**2 + j**2 + k**2)**(1/2))

print("M=", M)

print("This version is faster, so I set L to 100")
_ = input("Press any key when ready to continue")

from numpy import indices, sqrt

L = 101

I = indices([L, L, L])[0, :, :, :]  # x-axis
J = indices([L, L, L])[1, :, :, :]  # y-axis
K = indices([L, L, L])[2, :, :, :]  # z-axis

I[0, 0, 0] = 100  # to ensure that M[0,0,0] is not infinity

M = (1 - 2 * ((I+J+K) % 2))/sqrt(I**2+J**2+K**2)


axes = M[0, 0, 1:].sum() + M[0, 1:, 0].sum() + M[1:, 0, 0].sum()
faces = M[0, 1:, 1:].sum() + M[1:, 0, 1:].sum() + \
    M[1:, 1:, 0].sum()
off_axis = M[1:, 1:, 1:].sum()

madelung = (2 * axes) + (4 * faces) + (8 * off_axis)

print("M= ", madelung)
print("EXITING PROBLEM 2")

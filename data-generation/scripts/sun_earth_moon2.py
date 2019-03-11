# Exercise 6-17 part b
from numpy.linalg import solve
from math import*


r1 = 1000
r2 = 4000
r3 = 3000
r4 = 2000
I0 = 3*10**-9
Vplus = 5
Vt = .05


def f1(V1, V2):
    return (V1-Vplus)/r1 + V1/r2 + I0*(exp((V1-V2)/Vt)-1)


def f2(V1, V2):
    return (V2-Vplus)/r3 + V2/r4 + I0*(exp((V2-V1)/Vt)-1)


def df1dV1(V1, V2):
    return 1/r1 + 1/r2 + (I0/Vt)*exp((V1-V2)/Vt)


def df1dV2(V1, V2):
    return -(I0/Vt)*exp((V1-V2)/Vt)


def df2dV1(V1, V2):
    return -(I0/Vt)*exp((V2-V1)/Vt)


def df2dV2(V1, V2):
    return 1/r3 + 1/r4 + (I0/Vt)*exp((V2-V1)/Vt)


# Start with guess for V1 and V2
V1 = .65
V2 = .65
error = 10**-9

F = [[f1(V1, V2)], [f2(V1, V2)]]
M = [[df1dV1(V1, V2), df1dV2(V1, V2)], [df2dV1(V1, V2), df2dV2(V1, V2)]]

deltaV1, deltaV2 = solve(M, F)
deltaV1, deltaV2 = deltaV1[0], deltaV2[0]


while abs(deltaV1) > error or abs(deltaV2) > error:
    V1 -= deltaV1
    V2 -= deltaV2
    F = [[f1(V1, V2)], [f2(V1, V2)]]
    M = [[df1dV1(V1, V2), df1dV2(V1, V2)], [df2dV1(V1, V2), df2dV2(V1, V2)]]
    deltaV1, deltaV2 = solve(M, F)
    deltaV1, deltaV2 = deltaV1[0], deltaV2[0]
print(V1, V2)

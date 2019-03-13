# ============ PROBLEM 3 ============
print("ENTERING PROBLEM 3: Semi-Empirical Mass Formula")
print("P.3A")
_ = eval(input("Press any key when ready to continue"))
from numpy import sqrt


def binding_energy(A, Z):
    a1 = 15.67
    a2 = 17.23
    a3 = 0.75
    a4 = 93.2
    a5 = 0.
    if A % 2 == 1:
        a5 = 0.
    elif A % 2 == 0 and Z % 2 == 0:
        a5 = 12.
    elif A % 2 == 0 and Z % 2 == 1:
        a5 = -12.
    B = a1*A - a2*A**(2/3) - a3*Z**2/A**(1/3) - a4*(A-2*Z)**2/A + a5/sqrt(A)
    return B


A = 58
Z = 28
print(("binding energy: " + str(binding_energy(A, Z))))
print("PROBLEM 3.B")
_ = eval(input("Press any key when ready to continue"))
print(("binding energy per nucleon", str(binding_energy(A, Z)/A)))


print("PROBLEM 3.C")
_ = eval(input("Press any key when ready to continue"))


def binding_energy_most_stable(Z):
    a1 = 15.67
    a2 = 17.23
    a3 = 0.75
    a4 = 93.2
    a5 = 0.
    mostStable = -10000
    for A in range(Z, 3*Z+1, 1):
        if A % 2 == 1:
            a5 = 0.
        elif A % 2 == 0 and Z % 2 == 0:
            a5 = 12.
        elif A % 2 == 0 and Z % 2 == 1:
            a5 = -12.
        B = a1*A - a2*A**(2/3) - a3*Z**2/A**(1/3) - \
            a4*(A-2*Z)**2/A + a5/sqrt(A)
        if B/A > mostStable:
            mostStable = B/A
            stableA, stableB = A, B
    print(("mass number", stableA,
          "binding energy per nucleon", stableB/stableA, "MeV"))


binding_energy_most_stable(28)

print("PROBLEM 3.D")
_ = eval(input("Press any key when ready to continue"))

for Z in range(1, 101, 1):
    binding_energy_most_stable(Z)

print("max. binding energy: ")
binding_energy_most_stable(24)

print("EXITING PROBLEM 3")

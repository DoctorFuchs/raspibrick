from gpanel import *

makeGPanel(-10, 10, -10, 10)
pA = [0, 8]
pB = [0, -8]

for x in range(-9, 10, 1):
    pX = [x, 0]
    line(pA, pX)
    line(pB, pX)
keep()

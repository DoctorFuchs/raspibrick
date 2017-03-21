from gpanel import *

def isInSet(c):
    z = 0
    for n in range(maxIterations):
        z = z*z + c
        if abs(z) > R: # diverging
            return False
    return True

maxIterations = 50
R = 2
xmin = -2
xmax = 1
xstep = 0.03
ymin = -1.5
ymax = 1.5
ystep = 0.03

makeGPanel(xmin, xmax, ymin, ymax)
line(xmin, 0, xmax, 0)  # real axis
line(0, ymin, 0, ymax) # imaginary axis
title("Mandelbrot set")
y = ymin
while y <= ymax:
    x = xmin
    while x <= xmax:
        c = x + y*1j
        inSet = isInSet(c)
        if inSet:
            move(c)
            fillCircle(0.01)
        x += xstep
    y += ystep
keep()

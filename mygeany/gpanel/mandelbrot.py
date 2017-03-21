from gpanel import *

def getIterationColor(it):
    return [(30 * it) % 256, (4 * it) % 256, (255 - (30 * it)) % 256]

def mandelbrot(c):
    z = 0
    for it in range(maxIterations):
        z = z*z + c
        if abs(z) > R: # diverging
            return it
    return maxIterations

maxIterations = 50
R = 2
xmin = -2
xmax = 1
xstep = 0.003
ymin = -1.5
ymax = 1.5
ystep = 0.003

makeGPanel(xmin, xmax, ymin, ymax)
title("Mandelbrot Set")
enableRepaint(False)
y = ymin
while y <= ymax:
    x = xmin
    while x <= xmax:
        c = x + y*1j
        itCount = mandelbrot(c)
        if itCount == maxIterations: # inside Mandelbrot set
            setPenColor("black")
        else: # outside Mandelbrot set
           setPenColor(getIterationColor(itCount))
        point(c)
        x += xstep
    y += ystep
    repaint()
keep()


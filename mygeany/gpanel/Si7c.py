from gpanel import *

def f(z):
    return z * z + c

makeGPanel(-1.2, 1.2, -1.2, 1.2)
title("Mandelbrot iteration")

drawGrid(-1, 1.0, -1, 1.0, 4, 4, "gray")

isMandelbrot = askYesNo("c in Mandelbrot set?")
if isMandelbrot:
    c = 0.35 + 0.35j
    setColor("black")
else:
    c = 0.36+ 0.36j
    setColor("red")

title("Mandelbrot iteration with c = " + str(c))
move(c)
fillCircle(0.03)

z = 0j
while True:
    if z == 0:
        move(z)
    else:
        draw(z)
    z = f(z)
    delay(100)         


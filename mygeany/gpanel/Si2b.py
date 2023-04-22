
from gpanel import *

z = [9.6, 18.3, 29.0, 47.2, 71.1, 119.1, 174.6, 257.3, 350.7, 441.0, 513.3, 
559.7, 594.8, 629.4, 640.8, 651.1, 655.9, 659.6, 661.8]

def r(y):
    return r0 * (1 - y / m)

r0 = 0.62
y = 9.6
m = 662

makeGPanel(-2, 22, -100, 1100)
title("Bacterial growth")
drawGrid(0, 20, 0, 1000)
lineWidth(2)
for n in range(0, 19):
    move(n, z[n])
    setColor("black")
    fillCircle(0.2)
    if n > 0:
        dy = y * r(y)
        yNew = y + dy
        setColor("lime green")
        line(n - 1, y, n, yNew)
        y = yNew
keep()

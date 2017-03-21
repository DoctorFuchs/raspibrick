from gpanel import *

rx = 0.08
ry = 0.2
gx = 0.002
gy = 0.0004

def dx():
    return rx * x - gx * x * y

def dy():
    return -ry * y + gy * x * y
    
x = 500
y = 20

makeGPanel(-20, 220, -200, 2200)
title("Predator-Prey system (red: bunnies, blue: foxes)")
drawGrid(0, 200, 0, 2000)
lineWidth(2)
for n in range(200):
    xNew = x + dx()
    yNew = y + dy()
    setColor("red")
    line(n, x, n + 1, xNew)
    setColor("blue")
    line(n, y, n + 1, yNew)
    x = xNew
    y = yNew
keep()

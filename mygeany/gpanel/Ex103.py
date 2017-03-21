from gpanel import *
import math
import time

p = GPanel()
p.setUserCoords(-1, 11, -1.2, 1.2)
p.setPenColor("gray")
p.drawGrid(0, 10, -1.0, 1.0)
p.setPenColor(0, 0, 255)
p.setPenSize(2)

x = 0
T = 2
while x <= 10:
    if x == 0:
        p.pos(x, math.cos(math.pi / T * x))
    else:
        p.draw(x, math.cos(math.pi / T * x))
    x += 0.1
    time.sleep(0.1)
p.keep()

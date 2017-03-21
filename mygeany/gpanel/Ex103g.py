from gpanel import *
import math
import time

makeGPanel()
window(-1, 11, -1.2, 1.2)
setPenColor("gray")
drawGrid(0, 10, -1.0, 1.0)
setPenColor(0, 0, 255)
setPenSize(2)

x = 0
T = 2
while x <= 10:
    if x == 0:
        pos(x, math.cos(math.pi / T * x))
    else:
        draw(x, math.cos(math.pi / T * x))
    x += 0.1
    time.sleep(0.1)
keep()

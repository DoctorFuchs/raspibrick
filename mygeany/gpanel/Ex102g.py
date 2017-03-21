from gpanel import *
import math
import time

makeGPanel()
window(0, 10, -1.1, 1.1)
x = 0
T = 2
while x <= 10:
    if x == 0:
        move(x, math.cos(math.pi / T * x))
    else:
        draw(x, math.cos(math.pi / T * x))
    x += 0.1
    time.sleep(0.1)
keep()

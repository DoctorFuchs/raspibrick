from gpanel import *
import math
import time

p = GPanel(0, 10, -1, 1)
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

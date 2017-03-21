from gpanel import *
import math
import time
import sys

def onClose():
    sys.exit(0)
    
def measure():
    while True:
        clear()
        t = 0
        setPenColor("gray")
        drawGrid(0, 10, -1.0, 1.0)
        setPenColor("blue")
        while t <= 10:
            if t == 0:
                pos(0, 1)
            else:   
                draw(t, math.exp(-0.1 * t) * math.cos(math.pi / T * t))
            t += 0.1
            time.sleep(0.1)
                   
makeGPanel(-1, 11, -1.2, 1.2, close = onClose)
T = 2
run(measure)
keep()

from gpanel import *
import math
import time
import _thread, sys


def onClose():
    global isRunning
    sys.exit(0)
    
def measure():
    while True:
        p.clear()
        t = 0
        p.setPenColor("gray")
        p.drawGrid(0, 10, -1.0, 1.0)
        p.setPenColor("blue")
        while t <= 10:
            if t == 0:
                p.pos(0, 1)
            else:   
                p.draw(t, math.exp(-0.1 * t) * math.cos(math.pi / T * t))
            t += 0.1
            time.sleep(0.1)
                   
p = GPanel()
p.setUserCoords(-1, 11, -1.2, 1.2)
p.addCloseListener(onClose)
T = 2
_thread.start_new_thread(measure, ())
p.keep()

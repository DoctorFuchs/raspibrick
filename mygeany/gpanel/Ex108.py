# flickering

from gpanel import *

p = GPanel(-10, 110, -50, 50)
p.setPenColorStr("red")
forward = True
x = 0
while True:
    p.pos(x, 0)
    p.fillCircle(5)
    time.sleep(0.01)
    p.clear()
    if forward:
        x += 1
    else:    
        x -= 1
    if x == 100:
        forward = False
    if x == 0:
        forward = True        
p.keep()

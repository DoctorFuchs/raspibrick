# no flickering
# precise timing

from gpanel import *

p = GPanel(-10, 110, -50, 50)
p.setPenColorStr("red")
p.enableRepaint(False)
forward = True
x = 0
while True:
    startTime = time.clock()
    p.clear()
    p.pos(x, 0)
    p.fillCircle(5)
    p.repaint()
    if forward:
        x += 1
    else:    
        x -= 1
    if x == 100:
        forward = False
    if x == 0:
        forward = True        
    while (time.clock() - startTime)  < 0.01:
        pass
p.keep()

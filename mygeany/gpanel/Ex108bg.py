# no flickering
# precise timing

from gpanel import *

makeGPanel(-10, 110, -50, 50)
setPenColorStr("red")
enableRepaint(False)
forward = True
x = 0
while True:
    startTime = time.clock()
    clear()
    pos(x, 0)
    fillCircle(5)
    repaint()
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
keep()

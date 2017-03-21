# flickering

from gpanel import *

makeGPanel(-10, 110, -50, 50)
setPenColorStr("red")
forward = True
x = 0
while True:
    pos(x, 0)
    fillCircle(5)
    time.sleep(0.01)
    clear()
    if forward:
        x += 1
    else:    
        x -= 1
    if x == 100:
        forward = False
    if x == 0:
        forward = True        
keep()

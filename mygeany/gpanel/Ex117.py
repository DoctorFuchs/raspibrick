from gpanel import *

def onMousePressed(x, y):
    print("press event at", x, y)
    if p.isLeftMouseButton():
        p.setPenColor("red")
    else:
        p.setPenColor("green")
    p.pos(x, y)
    p.fillCircle(1)

p = GPanel()
p.setUserCoords(0, 100, 0, 100)
p.addMousePressListener(onMousePressed)
p.keep()

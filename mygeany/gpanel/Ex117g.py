from gpanel import *

def onMousePressed(x, y):
    print "press event at", x, y
    if isLeftMouseButton():
        setPenColor("red")
    else:
        setPenColor("green")
    pos(x, y)
    fillCircle(1)

makeGPanel()
setUserCoords(0, 100, 0, 100)
addMousePressListener(onMousePressed)
keep()

from gpanel import *

def onMousePressed(x, y):
    global isFirst
    if isLeftMouseButton():
        if isFirst:
            pos(x, y)
            startPath()
            isFirst = False
        else:
            draw(x, y)
        circle(0.01)
    if isRightMouseButton():
        fillPath("red")

makeGPanel(mousePressed = onMousePressed)
isFirst = True
keep()


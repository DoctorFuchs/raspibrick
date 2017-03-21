from gpanel import *

def onMousePressed(x, y):
    if isLeftMouseButton():
        pos(x, y)
    if isRightMouseButton():
        fill(x, y, "red")

def onMouseDragged(x, y):
    draw(x, y)

makeGPanel(mousePressed = onMousePressed,
           mouseDragged = onMouseDragged)
keep()


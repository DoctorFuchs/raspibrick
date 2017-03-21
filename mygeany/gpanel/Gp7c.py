from gpanel import *

def onMousePressed(x, y):
    pos(x, y)

def onMouseDragged(x, y):
    draw(x, y)

makeGPanel(mousePressed = onMousePressed,
           mouseDragged = onMouseDragged)
keep()


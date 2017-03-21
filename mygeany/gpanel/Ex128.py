# Rubberband lines

from gpanel import *

def onMousePressed(x, y):
    global x0, y0, x1, y1
    setXORMode()
    setPenColor("white")
    x0 = x1 = x
    y0 = y1 = y

def onMouseReleased(x, y):
    setPaintMode()
    setPenColor("black")
    line(x0, y0, x, y)    # draw final line

def onMouseDragged(x, y):
    global x1, y1
    line(x0, y0, x1, y1)  # erase old line
    line(x0, y0, x, y)    # draw new line
    x1 = x
    y1 = y

makeGPanel(mousePressed = onMousePressed, mouseReleased = onMouseReleased, 
           mouseDragged = onMouseDragged)
setPenSize(3)           
keep()

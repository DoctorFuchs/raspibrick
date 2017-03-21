from gpanel import *

def onKeyPressed(key):
    global x, y
    if key == Qt.Key_Left:
        x -= step
        drawCircle()
    elif key == Qt.Key_Right:
        x += step
        drawCircle()
    elif key == Qt.Key_Up:
        y += step
        drawCircle()
    elif key == Qt.Key_Down:
        y -= step
        drawCircle()

def drawCircle():
    move(x, y)
    setColor("green")
    fillCircle(5)
    setColor("black")
    circle(5)

makeGPanel(0, 100, 0, 100, keyPressed = onKeyPressed)
title("Move the circle with the arrow keys.")
x = 50
y = 50
step = 2
drawCircle()
keep()

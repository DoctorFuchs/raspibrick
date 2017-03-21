from gpanel import *

def updateGraphics():
    clear()
    line(pA, pB)
    line(pA, pC)
    r = 0
    while r <= 1:
        pX1 = getDividingPoint(pA, pB, r)
        pX2 = getDividingPoint(pA, pC, 1 - r)
        line(pX1, pX2)
        r += 0.05

def myCallback(x, y):
    pA[0] = x
    pA[1] = y
    updateGraphics()

makeGPanel(0, 100, 0, 100, 
              mousePressed = myCallback,
              mouseDragged = myCallback)

pA = [10, 10]
pB = [90, 20]
pC = [30, 90]
updateGraphics()
keep()

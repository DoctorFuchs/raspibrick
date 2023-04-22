from gpanel import *

def onKeyPressed(key):
    print("key press event:", key)

makeGPanel(0, 10, 0, 10, keyPressed = onKeyPressed)
text(1, 5, "Press any key.")
keep()

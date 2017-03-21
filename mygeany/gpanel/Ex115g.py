from gpanel import *
import random

makeGPanel(0, 100, 0, 100)
y = 90
x = random.randint(10, 90)
enableRepaint(False)
while True:
    clear()
    image("town.png", 0, 100)
    image("alieng.png", x, y)
    repaint()
    y -= 1
    if y < 20:
        y = 80
        x = random.randint(10, 90)
    time.sleep(0.01)
#keep()

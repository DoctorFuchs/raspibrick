from gpanel import *
import random

p = GPanel(0, 100, 0, 100)
y = 90
x = random.randint(10, 90)
p.enableRepaint(False)
while True:
    p.clear()
    p.image("town.png", 0, 100)
    p.image("alieng.png", x, y)
    p.repaint()
    y -= 1
    if y < 20:
        y = 80
        x = random.randint(10, 90)
    time.sleep(0.01)
p.keep()

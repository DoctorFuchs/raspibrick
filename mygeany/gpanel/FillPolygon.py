from gpanel import *
import random

NB_POLYGONS = 20
makeGPanel()
for i in range(NB_POLYGONS):
    setColor(getRandomX11Color())
    m = random.randint(5, 10)
    corners = []
    for k in range(m):
        x = random.random()
        y = random.random()
        corners.append([x, y])
    fillPolygon(corners)
    delay(100)
keep()

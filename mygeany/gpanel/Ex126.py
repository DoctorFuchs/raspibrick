from gpanel import *
import time

makeGPanel()
for i in range(20):
    setColor(getRandomX11Color())
    m = random.randint(5, 10)
    corners = []
    for k in range(m):
        x = random.random()
        y = random.random()
        corners.append([x, y])
    fillPolygon(corners)
storeGraphics() 
#saveGraphics()   
time.sleep(2)
clear()
time.sleep(2)
recallGraphics()
#restoreGraphics()
keep()

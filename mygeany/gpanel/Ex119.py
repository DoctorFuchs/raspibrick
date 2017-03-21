from gpanel import *
import time

p = GPanel(0, 10, 0, 10)
p.pos(5, 5)        
p.fillRectangle(8, 6)
time.sleep(2)
p.setWindowPos(300, 100)
time.sleep(2)
p.setWindowCenter()
p.keep()

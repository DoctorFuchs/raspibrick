from gpanel import *

p = GPanel()
p.setUserCoords(0, 10, 0, 10)
for ypt in range(0, 11, 1):
    p.line(0, ypt, 10 - ypt, 0)
    time.sleep(0.1) # to see what happens
p.keep()

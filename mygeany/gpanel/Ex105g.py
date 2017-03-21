from gpanel import *

makeGPanel(Size(600, 400))
setUserCoords(0, 10, 0, 10)
setBgColorStr("cyan")
title("Ex105")
#setTitle("Ex105")
for ypt in range(0, 11, 1):
    line(0, ypt, 10 - ypt, 0)
    time.sleep(0.1)
keep()

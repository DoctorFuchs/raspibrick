from gpanel import *

makeGPanel(0, 10, 0, 10)
setBgColor(0, 255, 255)
#setBgColorStr("cyan")
for ypt in range(0, 11, 1):
    line(0, ypt, 10 - ypt, 0)
    time.sleep(0.1)
keep()

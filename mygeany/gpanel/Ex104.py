from gpanel import *

p = GPanel(0, 10, 0, 10)
#p.setBgColor(0, 255, 255)
p.setBgColorStr("cyan")
for ypt in range(0, 11, 1):
    p.line(0, ypt, 10 - ypt, 0)
    time.sleep(0.1)
p.keep()

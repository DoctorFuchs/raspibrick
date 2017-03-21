from gpanel import *

p = GPanel(Size(600, 400))
p.setUserCoords(0, 10, 0, 10)
p.setBgColorStr("cyan")
p.setTitle("Ex105")
for ypt in range(0, 11, 1):
    p.line(0, ypt, 10 - ypt, 0)
    time.sleep(0.1)
p.keep()

from gpanel import *

p = GPanel(Size(600, 600))
p.setUserCoords(-10, 10, -10, 10)
p.setPenColorStr("red")
p.fillCircle(10)
p.setPenColorStr("black")
p.circle(10)
p.keep()

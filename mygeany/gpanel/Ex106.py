from gpanel import *

p = GPanel(Size(600, 400))
p.setUserCoords(-10, 10, -10, 10)
p.setPenColorStr("red")
p.fillCircle(5)
p.pos(8, 8)
p.setPenColorStr("black")
p.circle(1)
p.keep()

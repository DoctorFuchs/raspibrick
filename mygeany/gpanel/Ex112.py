from gpanel import *

p = GPanel(0, 100, 0, 100)
corners =[[10, 10], [80, 10], [40, 30], [20, 80]] 
#p.polygon(corners)
p.setPenColorStr("red")
p.fillPolygon(corners)
p.keep()

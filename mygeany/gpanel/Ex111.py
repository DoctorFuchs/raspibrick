from gpanel import *

p = GPanel(0, 100, 0, 100)
for x in range(100):
    p.point(x, 50)
#    p.pos(x, 50)
#    p.point()
p.keep()

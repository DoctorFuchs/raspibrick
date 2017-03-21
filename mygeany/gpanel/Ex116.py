from gpanel import *

p = GPanel(0, 10, 0, 10)
x1 = 2
y1 = 3
x2 = 8
y2 = 7
p.line(x1, y1, x2, y2)
d = p.getDividingPoint(x1, y1, x2, y2, 0.3)
print d
p.line(0, 0, d[0], d[1])
p.keep()

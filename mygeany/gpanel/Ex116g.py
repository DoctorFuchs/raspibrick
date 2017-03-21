from gpanel import *

makeGPanel(0, 10, 0, 10)
x1 = 2
y1 = 3
x2 = 8
y2 = 7
line(x1, y1, x2, y2)
d = getDividingPoint(x1, y1, x2, y2, 0.3)
print d
line(0, 0, d[0], d[1])
keep()

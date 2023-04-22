from gpanel import *

makeGPanel(0, 10, 0, 10)
pt1 = [2, 3]
pt2 = [8, 7]
line(pt1, pt2)
d = getDividingPoint(pt1, pt2, 0.3)
print(d)
line([0, 0], d)
keep()

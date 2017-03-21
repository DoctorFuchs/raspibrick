from gpanel import *

makeGPanel(0, 100, 0, 100)
     
pt1 = [10, 10]
pc1 = [20, 90]
pc2 = [70, 70]
pt2 = [90, 20]

setColor("green")

line(pt1, pc1)
line(pt2, pc2)
line(pc1, pc2)

r = 0
while r <= 1:
    q1 = getDividingPoint(pt1, pc1, r)
    q2 = getDividingPoint(pc1, pc2, r)
    q3 = getDividingPoint(pc2, pt2, r)
    line(q1, q2)
    line(q2, q3)
    r2 = getDividingPoint(q1, q2, r)
    r3 = getDividingPoint(q2, q3, r)
    line(r2, r3)
    r += 0.05

setColor("black")
#cubicBezier(pt1, pc1, pc2, pt2)    
keep()


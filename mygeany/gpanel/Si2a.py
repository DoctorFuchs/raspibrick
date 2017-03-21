from __future__ import division
from gpanel import *

# source: Swiss Federal Statistical Office, STAT-TAB
z2010 = 7870134 # Total 2010
z2011 = 7954662 # Total 2011
s2010 = 6103857 # Swiss 2010
s2011 = 6138668 # Swiss 2011

def drawGrid():
    # Horizontal
    for i in range(11):
        y = 2000000 * i
        line(0, y, 50, y)
        text(-3, y, str(2 * i))
    # Vertical
    for k in range(11):
        x = 5 * k
        line(x, 0, x, 20000000)
        text(x, -1000000, str(int(x + 2010)))

def drawLegend():
    setColor("lime green")
    y = 21000000
    move(0, y)
    draw(5, y)
    text("Swiss")
    setColor("red")
    move(15, y)
    draw(20, y)
    text("foreigner")
    setColor("blue")
    move(30, y)
    draw(35, y)
    text("Total")
    
makeGPanel(-5, 55, -2000000, 22000000)
title("Population growth extended")
drawGrid()
drawLegend()

a2010 = z2010 - s2010 # foreigners 2010
a2011 = z2011 - s2011 # foreigners 2011

lineWidth(3)
setColor("blue")
line(0, z2010, 1, z2011)
setColor("lime green")
line(0, s2010, 1, s2011)
setColor("red")
line(0, a2010, 1, a2011)

rs = (s2011 - s2010) / s2010  # Swiss growth rate
ra = (a2011 - a2010) / a2010  # foreigners growth rate

# iteration
s = s2011
a = a2011
z = s + a
sOld = s
aOld = a
zOld = z
for i in range(0, 49):
    s = s + rs * s  # model assumptions
    a = a + ra * a  # model assumptions
    z = s + a
    setColor("blue")
    line(i + 1, zOld, i + 2, z)
    setColor("lime green")
    line(i + 1, sOld, i + 2, s)
    setColor("red")
    line(i + 1, aOld, i + 2, a)
    zOld = z
    sOld = s
    aOld = a
keep()    


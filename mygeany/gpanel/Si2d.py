from __future__ import division
import exceptions
from gpanel import *

n = 10000 # size of the population

def readData(filename):
    table = []
    fData = open(filename)

    while True:
        line = fData.readline().replace(" ", "").replace("'", "")
        if line == "":
            break
        line = line[:-1] # remove trailing \n
        try:
            q = float(line)
        except exceptions.ValueError:
           break
        table.append(q)
    fData.close()
    return table

makeGPanel(-10, 110, -1000, 11000)
title("Population behavior/predictions  (blue -> male, red -> female)")
drawGrid(0, 100, 0, 10000)
qx = readData("qx.dat")
qy = readData("qy.dat")
x = n # males
y = n # females
for t in range(101):
    lineWidth(2)
    setColor("blue")
    rx = qx[t]
    x = x - x * rx
    line(t, 0, t, x)
    setColor("red")
    ry = qy[t]
    y = y - y * ry
    line(t + 0.2, 0, t + 0.2, y) 
keep()

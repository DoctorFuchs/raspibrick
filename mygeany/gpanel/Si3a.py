from __future__ import division
from gpanel import *
import random

n = 100 # size of the test  group
p = 0.5
z = 10000

def showDistribution():
    setColor("blue")
    lineWidth(5)
    for t in range(n + 1):
        line(t, 0, t, h[t])

def showMean():
    global mean
    sum = 0
    for t in range(n + 1):
        sum += h[t] * t
    mean = int(sum / z + 0.5)
    setColor("red")
    lineWidth(2)
    line(mean, 0, mean, 1000)
    text(mean - 1, -30, str(mean))

def showSpreading(level):
    sum = h[mean]
    for s in range(1, 20):
        sum += h[mean + s] + h[mean - s]
        if sum > z * level:
            break
    setColor("green")        
    lineWidth(2)
    line(mean + s, 0, mean + s, 1000)
    text(mean + s - 1, -30, str(mean + s))
    line(mean - s, 0, mean - s, 1000)
    text(mean - s - 1, -30, str(mean - s))

def sim():
    sum = 0
    for i in range(n):
       w = random.random()
       if w < p:
           sum +=1 
    return sum   

makeGPanel(-0.1 * n, 1.1 * n, -100, 1100)
title("Coin toss,  distribution of number")
drawGrid(0, 100, 0, 1000)
h = [0] * (n + 1) 

for i in range(z):
    k = sim()
    h[k] += 1

showDistribution()
showMean()
showSpreading(0.68)
showSpreading(0.95)
keep()




from gpanel import *
import random

n = 600 # number of tosses
p = 1 / 6
z = 10000
  
def showDistribution():
    setColor("blue")
    lineWidth(4)
    for i in range(21):
        line(i, 0, i, h[i])

def showLimit(level):
    sum = 0
    for i in range(21):
        sum += h[i]
        if sum > z * level: 
            break
    setColor("green")        
    lineWidth(2)
    line(i, 0, i, 2000)
    text(i, -80, str(i))
    return i

def chisquare(u):
    chisquare = 0
    e = n * p
    for i in range(1, 7):
        chisquare += ((u[i] - e) * (u[i] - e)) / e
    return chisquare

def sim():
    u = [0] * 7
    for i in range(n):
        t = random.randint(1, 6)
        u[t] += 1
    return chisquare(u)
        
makeGPanel(-2, 22, -200, 2200)
title("Chi-square simulation  is being carried out. Please wait...")
drawGrid(0, 20, 0, 2000)
h = [0] * 21

for i in range(z):
    c = int(sim())
    if c < 20:
        h[c] += 1
    else:
        h[20] += 1

title("Chi-square test on  the die")
showDistribution()
s = showLimit(0.95)

# Observed series
u1 = [0, 112, 128, 97, 103, 88, 72]
u2 = [0, 112, 108, 97, 113, 88, 82]
c1 = chisquare(u1)
c2 = chisquare(u2)
print("Die with", u1, "Xi-square:", c1, "loaded?", c1 > s)
print("Die with", u2, "Xi-square:", c2, "loaded?", c2 > s)
keep()


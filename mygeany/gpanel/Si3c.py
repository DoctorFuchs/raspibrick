from __future__ import division
from gpanel import *
import random

z = 10000
# survey values/polls
females_yes = 87
females_no = 19
males_yes = 62
males_no = 24

def showDistribution():
    setColor("blue")
    lineWidth(4)
    for i in range(101):
        line(i/10, 0, i/10, h[i])

def showLimit(level):
    sum = 0
    for i in range(101):
        sum += h[i]
        if sum > level * z: 
            break
    setColor("green")        
    lineWidth(2)
    limit = i / 10
    line(limit, 0, limit, 1000)
    text(limit, -80, str(limit))
    return limit

def chisquare(f0, f1, m0, m1):
    # f: females, m: males, 0:yes, 1:no
    w = (f0 + m0) / n # probability of a yes
    # expected value
    ef0 = (f0 + f1) * w # females-yes
    em0 = (m0 + m1) * w # males-yes
    ef1 = (f0 + f1) * (1 - w) # females-no
    em1 = (m0 + m1) * (1 - w) # males-no
    # add up deviations (u - e)*(u - e) / e
    chisquare = (f0 - ef0) * (f0 - ef0) / ef0 \
              + (m0 - em0) * (m0 - em0) / em0 \
              + (f1 - ef1) * (f1 - ef1) / ef1 \
              + (m1 - em1) * (m1 - em1) / em1
    return chisquare

def sim():
    # simulate females
    f0 = 0 # yes
    f1 = 0 # no
    for i in range(females_all):
        t = random.random()
        if t < p:
           f0 += 1 
        else:         
           f1 += 1 
    # simulate males
    m0 = 0 # yes
    m1 = 1 # no
    for i in range(males_all):
        t = random.random()
        if t < p:
           m0 += 1
        else:   
           m1 += 1  
    return chisquare(f0, f1, m0, m1)
    
females_all = females_yes + females_no
males_all = males_yes + males_no
n = females_all + males_all  # all
p = (females_yes + males_yes) / n  # probability of yes for all
print "Facebook yes (all):", round(100 * p, 1), "%"
pf = females_yes / females_all
print "Facebook yes (females):", round(100 * pf, 1), "%"
pm = males_yes / males_all
print "Facebook yes (males:)", round(100 * pm, 1), "%"

makeGPanel(-1, 11, -250, 2750)
title("Chi-square test, use of Facebook")
drawGrid(0, 10, 0, 2500)
h = [0] * 101

for i in range(z):
    c = int(10 * sim())  # magnification factor of 10
    if c < 100:
        h[c] += 1
    else:
        h[100] += 1

showDistribution()
s = showLimit(0.95)

c = chisquare(females_yes, females_no, males_yes, males_no)
print "critical value:", s
print "observed:", c,
if c <= s:
   print "- the same behavior"
else:
   print "- not the same behavior"
keep()

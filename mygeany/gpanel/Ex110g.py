from gpanel import *

makeGPanel(-10, 10, -10, 10)
setPenColorStr("red")
fillCircle(3)
for x in range(-10, 11): 
    c = getPixelColor(x, 0)
    print x, c

keep()

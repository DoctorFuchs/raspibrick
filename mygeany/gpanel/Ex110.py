from gpanel import *

p = GPanel(-10, 10, -10, 10)
p.setPenColorStr("red")
p.fillCircle(3)
for x in range(-10, 11): 
    c = p.getPixelColor(x, 0)
    print(x, c)

p.keep()

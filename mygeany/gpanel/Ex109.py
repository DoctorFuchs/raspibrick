from gpanel import *

p = GPanel(-10, 10, -10, 10)
p.setPenColor("red")
p.fillCircle(3)
#p.fill(0, 0, (255, 0, 0), (0, 255, 0))
p.fill(0, 0, "red", "green")

p.keep()

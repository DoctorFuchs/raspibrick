from gpanel import *
makeGPanel(-1.2, 1.2, -1.2, 1.2)
title("Complex plane")

z = 0.9 + 0.3j
for n in range(1, 60):
    y = z**n
    draw(y)
#fill(0.2, 0, [255, 255, 255], [255, 0, 0])
#fill(0.0, 0.2, [255, 255, 255], [0, 255, 0])
fill(0.2, 0, "red")
fill(0.0, 0.2, "green")
drawGrid(-1.0, 1.0, -1.0, 1.0)
keep()

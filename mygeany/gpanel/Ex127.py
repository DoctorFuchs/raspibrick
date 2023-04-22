from gpanel import *

makeGPanel()
setPenColor("white")

setXORMode()  
print("draw")
line(0.1, 0.1, 0.9, 0.9)
time.sleep(3)
print("redraw")
line(0.1, 0.1, 0.9, 0.9)
time.sleep(3)


setPenColor("black")
setPaintMode()  
print("draw")
line(0.1, 0.1, 0.9, 0.9)
time.sleep(3)
print("redraw")
line(0.1, 0.1, 0.9, 0.9)
time.sleep(3)

keep()

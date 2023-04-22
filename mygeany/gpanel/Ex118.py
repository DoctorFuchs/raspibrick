from gpanel import *

p = GPanel(0, 10, 0, 10)
print(p.getScreenHeight())
print(GPanel.getRandomX11Color())
p.pos(5, 5)        
p.rectangle(8, 6)
#p.rectangle(1, 2, 9, 8)
p.keep()

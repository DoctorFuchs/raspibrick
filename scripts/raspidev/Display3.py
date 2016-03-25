# Display2.py

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
dp.showTicker("IPx 192-168-82-43", count = 3, speed = 2, blocking = True)
dp.showText("donE")
time.sleep(3)
dp.clear()
print "All done"

# Display6a.py
# Ticker test, ctor parameter

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
ip = "x192-168-1-13"
dp.showTicker(ip, count = 2, speed = 4, blocking = True)
time.sleep(3)
dp.showText("IdLE")
time.sleep(3)
dp.clear()
print "all done"

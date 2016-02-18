# Display6b.py
# Ticker test, infinite duration

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
ip = "x192-168-1-13"
dp.showTicker(ip, count = 0)
print "Sleeping now..."
time.sleep(10)
dp.stopTicker()
time.sleep(3)
dp.showText("IdLE")
time.sleep(3)
dp.clear()
print "all done"

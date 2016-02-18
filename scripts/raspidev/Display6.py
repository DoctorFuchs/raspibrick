# Display6.py
# Ticker test, default ctor

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
ip = "x192-168-1-13"
dp.showTicker(ip)
while dp.isTickerAlive():
    continue
dp.showText("IdLE")
time.sleep(3)
dp.clear()
print "all done"

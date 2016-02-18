# Display7.py
# Blinker test, default ctor

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
text = "boot"
dp.showBlinker(text)
while dp.isBlinkerAlive():
    continue
time.sleep(3)
dp.showText("Bye")
time.sleep(3)
dp.clear()
print "all done"

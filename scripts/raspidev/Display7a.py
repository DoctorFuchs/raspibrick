# Display7a.py
# Blinker test, ctor params

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
text = "boot"
dp.showBlinker(text, dp = [0, 0, 0, 1], count = 4, speed = 2, blocking = True)
print "all done"

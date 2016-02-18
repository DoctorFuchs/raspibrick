# Display1.py

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
dp.setDigit('A', 0)
time.sleep(3)
dp.showText("1234")
time.sleep(3)
dp.showText("1234567890")
time.sleep(3)
dp.showText("1234567890", pos = 2)
time.sleep(3)
dp.showText("1234567890", pos = -2)
time.sleep(3)
dp.showText("1234567890", pos = 1, dp = [1, 1, 0])
time.sleep(3)
dp.showText("1234567890", pos = 1, dp = [0, 1])
time.sleep(3)
dp.clear()
print "All done"

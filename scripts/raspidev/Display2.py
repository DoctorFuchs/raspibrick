# Display2.py

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()
dp.showText("run")
time.sleep(3)
for i in range(10000):
    dp.showText("%4d" %i) # right adjusted
    time.sleep(0.005)
time.sleep(3)
dp.showText("donE")
time.sleep(3)
# necessary to stop internal multiplexer thread
#dp.clear()
print "All done"

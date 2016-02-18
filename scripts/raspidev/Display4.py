# Display4.py
# Scroll text to right

from Disp4tronix import Disp4tronix
import time

dp = Disp4tronix()

text = "0123456789"
print "show text with", text
#rc = dp.showText(text)
rc = dp.showText(text, 2)
#rc = dp.showText(text, pos = -2)
time.sleep(3)
for i in range(10):
    nb = dp.scrollToRight()
    print "remaining:", nb
    time.sleep(2)
dp.clear()
print "done"

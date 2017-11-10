# Display5c.py
# Scroll left

from TM1637 import FourDigit
from time import sleep
        
d = FourDigit()
d.show("0123456789")
sleep(2)
for i in range(10):
    d.toLeft()
    sleep(1)
d.show("donE")
# Display5d.py
# Scroll right

from TM1637 import FourDigit
from time import sleep
        
d = FourDigit()
d.show("0123456789")
sleep(2)
for i in range(4):
    d.toRight()
    sleep(1)
d.toStart()
sleep(1)
d.show("donE")
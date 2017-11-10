# Display5b.py
# Shift

from TM1637 import FourDigit
from time import sleep
        
d = FourDigit()
d.show("0123")
sleep(2)
d.show("0123", 2)
sleep(2)
d.show("0123", -2)
sleep(2)
d.show("donE")
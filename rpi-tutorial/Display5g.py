# Display5g.py
# Example scrolling text

from TM1637 import FourDigit
from time import sleep
        
d = FourDigit()
d.show("HELLo PYthon")
sleep(1)
while True:
    nb = 1
    while nb > 0:
        nb = d.toLeft()
        sleep(0.5)
    sleep(1)
    d.toStart()     
    sleep(1)

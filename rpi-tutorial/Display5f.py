# Display5f.py
# Return value from toRight

from TM1637 import FourDigit
from time import sleep
        
d = FourDigit()
d.show("0123456789")
sleep(2)
nb = 1
while nb > 0:
    nb = d.toRight()
    print(nb)
    sleep(1)
d.show("donE")
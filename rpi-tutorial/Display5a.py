# Display5a.py

from TM1637 import FourDigit
from time import sleep
        
d = FourDigit()
d.erase()
sleep(2)
d.show("0123")
sleep(3)
d.setColon(True)
d.show("ABCD")
sleep(3)
d.setColon(False)
d.setLuminosity(7) # range 0..7
d.show("donE")
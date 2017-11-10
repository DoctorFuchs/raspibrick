# Display5i.py
# count 

from TM1637 import FourDigit
        
d = FourDigit()

while True:
    for n in range(10000):
        d.show(n)


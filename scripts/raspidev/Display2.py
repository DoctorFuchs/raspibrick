# Display2.py

from Disp4tronix import Disp4tronix

print "Displayable:", Disp4tronix.getDisplayableChars()
dp = Disp4tronix()
k = 32

while k < 128:
    print "<cr> or x<cr> to terminate",
    text = raw_input()	# Fetch the input from the terminal
    if text == "x":
        break
    s = chr(k) + chr(k+1) + chr(k+2) + chr(k+3)
    print k, s
    dp.showText(s)
    k += 4

dp.clear()
print "All done"

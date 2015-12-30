# ShowIP.py

from raspibrick import *

robot = Robot()
display = Display()

ipAddr = robot.getIPAddresses()
ip = ""
for addr in ipAddr:
    if addr != '127.0.0.1':
        ip += addr
        ip += "    "
ip = ip.replace(".", "-")

if display.isAvailable():
    print "IP address:", ip
    display.showTicker("x" + ip, 2, 1)
    while display.isTickerAlive():
        Tools.delay(100)
robot.exit()

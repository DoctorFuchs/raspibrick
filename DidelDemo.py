# DidelDemo.py

from raspibrick import *
import time

display = DgTell(0x24)
if display.isAvailable():
    text = "boot"
    display.showText(text)
    time.sleep(4)

    text = "Dg4TeLLi2c by j-d nicoud"
    display.showTicker(text, count = 2, speed = 2, blocking = True)

    ipAddr = MyRobot.getIPAddresses()
    ip = ""
    for addr in ipAddr:
        if addr != '127.0.0.1':
            ip += "#"
            ip += addr
            ip += "    "
    ip = ip.replace(".", "-")

    if ip == "":
        text = "noIP"
    else:
        text = "IP"
    display.showText(text)
    time.sleep(4)

    if ip != "":
        display.showTicker(ip, count = 2, speed = 1, blocking = True)

    text = "8YE"
    display.showBlinker(text, dp = [0, 0, 1, 0], count = 4, speed = 2, blocking = True)
else:
    print "Display not available at i2c address 0x24"

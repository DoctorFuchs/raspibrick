# RenameHost.py

import sys
from raspibrick import *
import os, subprocess

fname = "/mnt/recovery/raspibrick-rename.requested"
if not os.path.isfile(fname):
    print("RenameHost tag file not found")
    sys.exit()

fInp = open(fname)
hostname = fInp.readline()
fInp.close()
print("New host name:", hostname)
robot = Robot()
display = Display()
display.showTicker("CHG HOST", 1, 1, True)

subprocess.call("sudo /home/pi/raspibrick/rename-host " + hostname, shell=True)
os.remove(fname)
display.showText("boot")

Tools.delay(2000)
robot.exit()
os.system("sudo shutdown -r now")
# ProcessMon.py
# Do not use robot instance unless for quitting

from Tools import Tools
from raspibrick import *
import os, subprocess
import BrickGateProperties


# ------------------------- main ------------------------------------
print "ProcessMon " + SharedConstants.VERSION + " starting"
Tools.delay(1000)  # Wait until raspi is up

# Check if update requested
fname = "/mnt/recovery/raspibrick-update.requested"
if os.path.isfile(fname):
    print "Update requested"
    robot = Robot()
    display = Display()
    led = Led(1)
    display.setText("UPE ", [1, 0, 0])
    for i in range(3):
        led.setColor(0, 0, 0)
        Tools.delay(500)
        led.setColor(10, 10, 10)
        Tools.delay(500)
    subprocess.call("sudo update-raspibrick", shell = True)
    os.remove(fname)
    display.setText("boot")
    Tools.delay(3000)
    display.clear()
    led.setColor(10, 0, 0)
    print "Update done. Shutting down now"
    Tools.delay(2000)
    os.system("sudo shutdown -r now")
else:
    isRunning = True
    isFirst = True
    while isRunning:
        print "Spawning IdleProc..."
        if isFirst:
            arg = "isFirst"
            isFirst = False
        else:
            arg = "isNotFirst"
        # Blocking call
        rc = subprocess.call(["pyrun", "/home/pi/raspibrick/IdleProcess.py", arg])
        print "Returning from IdleProc with exit code:", rc
        if rc == 1 or rc > 10:
            pythonApp = "/home/pi/scripts/MyApp.py"
            if os.path.isfile(pythonApp):
               print "Spawning user app " +  pythonApp
               rc = subprocess.call(["pyrun", pythonApp])
               # return value not used yet
               print "Returning from MyApp with exit code:", rc
            else:
               print "No Python app found to execute"
        elif rc == 2:
            print "Spawning BrickGate server..."
            rc = subprocess.call(["pyrun", "/home/pi/raspibrick/BrickGate.py"])
            print "Returning from BrickGate with exit code:", rc
        elif rc == 3:
            print "Shutting down now..."
            isRunning = False
    print "Shutdown process starting..."
    robot = Robot()
    display = Display()
    led = Led(1)
    display.setText("8YE ", [1, 0, 0])
    Tools.delay(3000)
    display.clear()
    led.setColor(20, 0, 0)
    Tools.delay(2000)
    os.system("sudo shutdown -h now")






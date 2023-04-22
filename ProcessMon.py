# ProcessMon.py
# Do not use robot instance unless for quitting

from raspibrick import *
import os, subprocess
import RPi.GPIO as GPIO
from OLED1306 import OLED1306

def showOled(text, lineNum, fontSize, indent, clear = False):
    if oled == None:
        return
    if clear:
        oled.clear()
    oled.setText(text, lineNum, fontSize, indent)

unit = 100

# ------------------------- main ------------------------------------
print("ProcessMon " + SharedConstants.VERSION + " starting")
Tools.delay(1000)  # Wait until raspi is up
fname = "/home/pi/scripts/autostart.py"
if os.path.isfile(fname):
     print("Found:", fname, "and run it now...")
     subprocess.Popen(["pyrun",  fname])
     sys.exit(0)

print("Check Pi2Go or Standalone mode...")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(SharedConstants.P_BUTTON, GPIO.OUT)
GPIO.output(SharedConstants.P_BUTTON, GPIO.HIGH)  # to ensure it is HIGH
GPIO.setup(SharedConstants.P_BUTTON, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(SharedConstants.P_BATTERY_MONITOR, GPIO.IN, GPIO.PUD_DOWN)
Tools.delay(1000)
# Check if standalone mode is requested
# if Pi2Go is available, the P_BATTERY_MONITOR is HIGH, assumes
# that standalone mode is requested if the pin is LOW (because of pull-down)
# if the pin is HIGH (Pi2Go present), the P_BUTTON must be LOW to escape (held down
# when Pi2Go boots to manually escape to standalone mode)
if  GPIO.input(SharedConstants.P_BATTERY_MONITOR) == GPIO.LOW:
    print("Pin 18 LOW (open). Escaping to standalone mode")
    GPIO.cleanup()
    Tools.delay(2000)
    sys.exit(0)
else:
    print("Pi2Go mode assumed.")

# Check if update requested
fname = "/mnt/recovery/raspibrick-update.requested"
if os.path.isfile(fname):
    print("Update requested")
    robot = Robot()
    display = Display()
    display.showText("UPE ")
    showOled("Update requested", 0, 15, 0, True)
    led = Led(1)
    for i in range(3):
        led.setColor(0, 0, 0)
        Tools.delay(500)
        led.setColor(10, 10, 10)
        Tools.delay(500)
    subprocess.call("sudo update-raspibrick", shell = True)
    os.remove(fname)
    display.showText("boot")
    showOled("Booting now...", 0, 15, 0, True)
    Tools.delay(3000)
    display.clear()
    if oled != None:
        oled.clear()
    led.setColor(10, 0, 0)
    print("Update done. Shutting down now")
    Tools.delay(2000)
    os.system("sudo shutdown -r now")
else:
    isRunning = True
    isFirst = True
    oled = OLED1306("/home/pi/Pictures/pi2go.ppm")
    if not oled.isDeviceAvailable():
        oled = None
    if oled != None:
        oled.setText("Welcome", 0, 15, 58) 
        oled.setText("to the", 1, 15, 80) 
        oled.setText("Pi2Go", 2, 15, 80) 
        Tools.delay(4000)
        oled.setBkImage(None)
    while isRunning:
        print("Spawning IdleProc...")
        if isFirst:
            arg = "isFirst"
            isFirst = False
        else:
            arg = "isNotFirst"
        # Blocking call
        rc = subprocess.call(["pyrun", "/home/pi/raspibrick/IdleProcess.py", arg])
        print("Returning from IdleProc with exit code:", rc)
        if rc == 1 or rc > 10:
            showOled("Starting program", 3, 12, 0, True)
            pythonApp = "/home/pi/scripts/MyApp.py"
            if os.path.isfile(pythonApp):
               print("Spawning user app:", pythonApp)
               rc = subprocess.call(["pyrun", pythonApp])
               # return value not used yet
               print("Returning from MyApp with exit code:", rc)
            else:
               print("No Python app found to execute")
        elif rc == 2:
            print("Spawning BrickGate server...")
            if oled != None:
	        showOled("Starting", 2, 10, 0, True)
                showOled("BrickGate server", 4, 12, 0, False)
                Tools.delay(2000)
            rc = subprocess.call(["pyrun", "/home/pi/raspibrick/BrickGate.py"])
            print("Returning from BrickGate with exit code:", rc)
        elif rc == 3:
            print("Shutting down now...")
            isRunning = False
    print("Shutdown process starting...")
    robot = Robot()
    display = Display()
    display.showBlinker("8YE", count = 2, speed = 2, blocking = True)
    showOled("Goodbye...", 0, 15, 0, True) 
    led = Led(1)
    led.setColor(20, 0, 0)
    Tools.delay(2000)
    os.system("sudo shutdown -h now")






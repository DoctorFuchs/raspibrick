# ProcessMon.py
# Do not use robot instance unless for quitting

from raspibrick import *
import os, subprocess
import RPi.GPIO as GPIO
import ConfigParser

def getConfigEntry(section, key):
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read(SharedConstants.CONFIG_FILE)
    try:
        value = config.get(section, key)
    except:
        return None
    return value

def setConfigEntry(section, key, value):
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    if not os.path.isfile(SharedConstants.CONFIG_FILE):
        config.add_section(section)
        config.set(section, key, value)
        with open(SharedConstants.CONFIG_FILE, 'wb') as configFile:
            config.write(configFile)
    else:
        config.read(SharedConstants.CONFIG_FILE)
        sections = config.sections()
        if not section in sections:
            config.add_section(section)
        config.set(section, key, value)
        with open(SharedConstants.CONFIG_FILE, 'wb') as configFile:
            config.write(configFile)

# ------------------------- main ------------------------------------
print "ProcessMon " + SharedConstants.VERSION + " starting"
Tools.delay(1000)  # Wait until raspi is up
print "Check button"
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(SharedConstants.P_BUTTON, GPIO.OUT)
GPIO.output(SharedConstants.P_BUTTON, GPIO.HIGH)  # to ensure it is HIGH
GPIO.setup(SharedConstants.P_BUTTON, GPIO.IN, GPIO.PUD_UP)
Tools.delay(1000)
if  GPIO.input(SharedConstants.P_BUTTON) == GPIO.LOW:
    robot = Robot()
    display = Display()
    led = Led(1)
    mode = getConfigEntry("Firmware", "Mode")
    print "Checking mode...Got:", mode
    if mode == "self" or mode == None:
        setConfigEntry("Firmware", "Mode", "auto")
        print "Setting new mode: 'auto'"
        display.showText("Auto")
        led.setColor(0, 0, 50)
    else:
        setConfigEntry("Firmware", "Mode", "self")
        print "Setting new mode: 'self'"
        display.showText("5ELF")
        led.setColor(0, 50, 0)
    Tools.delay(3000)
    display.clear()
    led.clearAll()
    sys.exit(0)

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
        if rc == 4 or rc == 139:  # mode 'self'
            print "Terminating Python now..."
            sys.exit(0)
        elif rc == 1 or rc > 10:
            pythonApp = "/home/pi/scripts/MyApp.py"
            if os.path.isfile(pythonApp):
               print "Spawning user app:", pythonApp
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
    display.showBlinker("8YE", count = 2, speed = 2, blocking = True)
    led = Led(1)
    led.setColor(20, 0, 0)
    Tools.delay(2000)
    os.system("sudo shutdown -h now")






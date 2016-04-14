# ProcessMon.py
# Do not use robot instance unless for quitting

from raspibrick import *
import os, subprocess
import RPi.GPIO as GPIO

unit = 100

morse = {
'a':'.-'   , 'b':'-...' , 'c':'-.-.' , 'd':'-..'  , 'e':'.'    ,
'f':'..-.' , 'g':'--.'  , 'h':'....' , 'i':'..'   , 'j':'.---' ,
'k':'-.-'  , 'l':'.-..' , 'm':'--'   , 'n':'-.'   , 'o':'---'  ,
'p':'.--.' , 'q':'--.-' , 'r':'.-.'  , 's':'...'  , 't':'-'    ,
'u':'..-'  , 'v':'...-' , 'w':'.--'  , 'x':'-..-' , 'y':'-.--' ,
'z':'--..' , '1':'.----', '2':'..---', '3':'...--', '4':'....-',
'5':'.....', '6':'-....', '7':'--...', '8':'---..', '9':'----.',
'0':'-----', '-':'-....-', '?':'..--..', ',':'--..--', ':':'---...',
'=':'-...-'}

def emitDot():
    buzz(True)
    Tools.delay(unit)
    buzz(False)

def emitDash():
    buzz(True)
    Tools.delay(3 * unit)
    buzz(False)

def transmit(text):
    for c in text:
        if c == " ":
            Tools.delay(7 * unit)
        else:
            c = c.lower()
            if c in morse:
                k = morse[c]
                for x in k:
                    if x == '.':
                        emitDot()
                    else:
                        emitDash()
                    Tools.delay(unit)
            Tools.delay(3 * unit)

def buzz(on):
    if on:
        GPIO.output(SharedConstants.P_BUZZER, GPIO.HIGH)
    else:
        GPIO.output(SharedConstants.P_BUZZER, GPIO.LOW)

def playIP(ip):
    transmit(ip)

# ------------------------- main ------------------------------------
print "ProcessMon " + SharedConstants.VERSION + " starting"
Tools.delay(1000)  # Wait until raspi is up
print "Check button"
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(SharedConstants.P_BUZZER, GPIO.OUT)
GPIO.setup(SharedConstants.P_BUTTON, GPIO.OUT)
GPIO.output(SharedConstants.P_BUTTON, GPIO.HIGH)  # to ensure it is HIGH
GPIO.setup(SharedConstants.P_BUTTON, GPIO.IN, GPIO.PUD_UP)
Tools.delay(1000)
# Check if standalone modus is requested
if  GPIO.input(SharedConstants.P_BUTTON) == GPIO.LOW:
    print "Button is pressed. Escaping to standalone mode"
    robot = Robot()
    ipAddr = robot.getIPAddresses()
    print "Got IP addresses:", ipAddr
    ip = ""
    for addr in ipAddr:
        if addr != '127.0.0.1':
            ip += addr
            ip += "    "
    if ip == "":
        ip = "0.0.0.0    "
    ip = ip.replace(".", "-")
    display = Display()
    if display.isAvailable():
        display.showTicker("x" + ip, 1, 1)
    idx = ip.rfind('-')
    lastNb = ip[idx + 1:].strip()
    playIP("ip " + lastNb)
    while display.isTickerAlive():
        time.sleep(0.1)
    if display.isAvailable():
        display.showText("donE")
        Tools.delay(2000)
        display.clear()
    robot.exit()
    Tools.delay(2000)
    sys.exit(0)
else:
    print "Button is not pressed!"

# Check if update requested
fname = "/mnt/recovery/raspibrick-update.requested"
if os.path.isfile(fname):
    print "Update requested"
    robot = Robot()
    display = Display()
    led = Led(1)
    display.showText("UPE ")
    for i in range(3):
        led.setColor(0, 0, 0)
        Tools.delay(500)
        led.setColor(10, 10, 10)
        Tools.delay(500)
    subprocess.call("sudo update-raspibrick", shell = True)
    os.remove(fname)
    display.showText("boot")
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






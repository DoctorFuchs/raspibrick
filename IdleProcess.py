# IdleProcess.py
# The application to execute is always MyApp.py (path defined in SharedConstants.APP_PATH)
# To SFTP download always overwrites this file. The main process detects this new download
#  because its creation date it NOT 0 (1-1-1970 01:00:00).
# A file update is started that copies all MyApp_n.py to MyApp_(n+1).py with n = 8, 7,..,1 ,
# then copies MyApp.py to MyApp_1.py and sets creation time of MyApp.py to zero.

# The app selection performed with a double-click copies the current selected app to
# MyApp.py and sets its creation time to zero. So no update process is started. The current
# selected file name (including the file ID) is stored in a configuration file

# The file execution performed by a single click stops the current IdleProcess and resumes
# ProcessMonitor.py that executes MyApp.py. When the application terminates, ProcessMonitor.py
# resumes and restarts IdleProcess.py that remembers the application file ID and displays it,
# so the same app can be started again.

import os.path
import shutil
import configparser
import _thread

from raspibrick import *

def showOled(text, lineNum, fontSize, indent, clear = False):
    if robot.displayType != "oled":
        return
    if clear:
        robot.oled.clear()
    robot.oled.setText(text, lineNum, fontSize, indent)

def blinker(nb):
    for i in range(nb):
        led.setColor(0, 0, 0)
        time.sleep(0.2)
        led.setColor(0, 0, 50)
        time.sleep(0.2)

def ledBlink(nb):
    _thread.start_new_thread(blinker, (nb,))

def showAppInfo(forceUpdate):
    global oldText
    if nbProg > 0:
        text = "P" + str(progID) + "-" + str(nbProg)
        text1 = "P" + str(progID) + " of " + str(nbProg)
    else:
        text = "P0-0"
        text1 = "No program"
    if oldText != text or forceUpdate:
        display.showText(text)
        showOled(text1, 0, 15, 0, True)
        if nbProg > 0:
            showOled("Click to execute pgm", 2, 10, 0, False)
            showOled("DClick to select next pgm", 3, 10, 0, False)
        showOled("LPress to start BrickGate", 4, 10, 0, False)
        oldText = text

def showIPAddress():
    ipAddr = robot.getIPAddresses()
    ip = ""
    for addr in ipAddr:
        if addr != '127.0.0.1':
            ip += addr
            ip += "   "
    ipx = ip.replace(".", "-")
    display.showTicker("x" + ipx, 1, 1, True)
    if robot.displayType == "oled":
        if ip == "":
            showOled("Current IP address", 0, 10, 0, True)
            showOled("0.0.0.0", 1, 15, 0)
        else:
            showOled("Current IP address:", 0, 10, 0, True)
            msg = ip.split("   ")
            for i in range (len(msg)):
                showOled(msg[i], i + 1, 15, 0)
        Tools.delay(3000)
    showAppInfo(True)

def updateAppFiles():
    global nbProg, progID, showUpdateInfo
    Tools.debug("Calling updatAppFiles()")
    if inCallback:
        Tools.debug("updateAppFiles() returned because inCallback = True")
        return

    # Check if MyApp.py has changed using time stamp
    file0 = SharedConstants.APP_PATH + ".py"
    file1 = SharedConstants.APP_PATH + "_1.py"
    if not os.path.isfile(file0):
        nbProg = 0
        progID = 0
        showAppInfo(False)
        return

    if os.path.isfile(file0) and int(os.path.getmtime(file0)) != 0: # file exists and time of modificaton not zero
        Tools.debug("Update needed")
        if showUpdateInfo:
	    display.showText("P---")
            showOled("New program", 0, 12, 0, True)
            showOled("detected", 1, 12, 0, False)
            Tools.delay(3000)  # if download and execute, the process is killed here
        showUpdateInfo = True         
        for i in reversed(list(range(1, 9))):
            file_old = SharedConstants.APP_PATH + "_" + str(i) + ".py"
            file_new = SharedConstants.APP_PATH + "_" + str(i + 1) + ".py"
            copyFile(file_old, file_new)
        copyFile(file0, file1)
        Tools.debug("Set timestamp to zero")
        os.utime(file0, (0, 0))  # set time of modification to zero
        nbProg = getNbProg()
        progID = 1
        showAppInfo(True)
        setConfigEntry("Programs", "LastProgram", "MyApp_1.py")

def copyFile(src, dst, attr = False):
    try:
        shutil.copyfile(src, dst)
        if attr:
            shutil.copystat(src, dst)
    except:
#       print "Error copying", src, " to", dst
       return False
#    print "Successfully copied", src, " to", dst
    return True

def getNbProg():
    for i in range(1, 11):
      if not os.path.isfile(SharedConstants.APP_PATH + "_" + str(i) + ".py"):
          break
#    print "getNbProg() returns", i - 1
    return i - 1

def onButtonEvent(event):
    global rc, inCallback, isAlive, nbProg, progID
    global isShutdownPending, isInterrupted
    isInterrupted = True
    if not isAlive or display.isTickerAlive():
        return
    inCallback = True
    if event == BUTTON_PRESSED:
        if isShutdownPending:
#            print "shutdown is pending"
            if ir_center.getValue() == 1:
               rc = 3
               isAlive = False
               return

    elif event == BUTTON_CLICKED:
        if isShutdownPending and ir_center.getValue() == 0:
            isShutdownPending = False
#            print "shutdown pending released"
            led.setColor(0, 0, 100)
            showAppInfo(True)
            inCallback = False
            return
        if ir_center.getValue() == 1:
            showIPAddress()
            inCallback = False
            return
        if progID == 0: # no app
            pass
#            print "no program"
        else:
            rc = 1
            isAlive = False

    elif event == BUTTON_DOUBLECLICKED:
        if nbProg == 0:
            inCallback = False
            return
        if nbProg > 0 and ir_center.getValue() == 1:
#            print "delete all"
            display.showText("dEL")
            showOled("All programs", 0, 15, 0, True)
            showOled("deleted", 1, 15, 0, False)
            time.sleep(1)
            try:
                for i in range(1, nbProg + 1):
                    os.remove(SharedConstants.APP_PATH + "_" + str(i) + ".py")
                os.remove(SharedConstants.APP_PATH + ".py")
                os.remove(SharedConstants.CONFIG_FILE)
            except:
                pass
            nbProg = 0
            progID = 0
            inCallback = False
            return
        if progID == nbProg:
            progID = 1
        else:
            progID += 1
#        print "progID", progID
        file0 = SharedConstants.APP_PATH + ".py"
        file1 = SharedConstants.APP_PATH + "_" + str(progID) + ".py"
        copyFile(file1, file0)
        os.utime(file0, (0, 0))  # set to zero to inhibit update
        showAppInfo(True)
        setConfigEntry("Programs", "LastProgram", "MyApp_" + str(progID) + ".py")
        ledBlink(progID)
    elif event == BUTTON_LONGPRESSED:
#        print "Button long pressed"
        if ir_center.getValue() == 1:
            if not isShutdownPending:
                isShutdownPending = True
                display.showText("oooo")
                showOled("Shutdown", 0, 15, 0, True)
                showOled("Are you sure?", 1, 10, 1, False)
                led.setColor(100, 0, 0)
        else:  # starting BrickGate
            isShutdownPending = False
            rc = 2
            isAlive = False
    inCallback = False

def firstDuty():
    display.showText("E" + SharedConstants.DISPLAYED_VERSION, 0, [0, 1, 0])
    showOled("Starting RaspiBrick", 0, 10, 0)
    showOled("V" + SharedConstants.VERSION, 1, 15, 0) 
    showOled("Searching access point", 2, 10, 0)
    Tools.delay(4000)
    display.showText("AP--")
    count = 0
    ip = ""
    robot.setButtonEnabled(True)
    while not isInterrupted and count < 40:  # Try 20 s to get IP address
       ipAddr = robot.getIPAddresses()
#       print "Got IP addresses:", ipAddr
       ip = ""
       for addr in ipAddr:
           if addr != '127.0.0.1':
              ip += addr
              ip += "    "
       if ip != "":
           break
       count += 1
       Tools.delay(500)
    display.clear()
    if ip == "":
#        print "No IP address received"
        led.setColor(10, 10, 0)
    else:
        led.setColor(0, 20, 0)

    if ip == "":
        showOled("Got IP address", 2, 10, 0)
        showOled("0.0.0.0", 3, 15, 0)
    else:
        showOled("Got IP address:", 2, 10, 0)
        showOled(ip, 3, 15, 0)
 
    if display.isAvailable():
        if not isInterrupted and display.isAvailable():
            if ip == "":
                ip = "0.0.0.0    "
            ip = ip.replace(".", "-")
            display.showTicker("x" + ip, 3, 1)
            while not isInterrupted and display.isTickerAlive():
                Tools.delay(1000)
            display.stopTicker()
    else:
        Tools.delay(3000)
    Beeper().beep(2)


def getConfigEntry(section, key):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(SharedConstants.CONFIG_FILE)
    try:
        value = config.get(section, key)
    except:
        return None
    return value

def setConfigEntry(section, key, value):
    config = configparser.ConfigParser()
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

def blinkLed():
    for i in range(3):
        led.setColor(0, 0, 0)
        Tools.delay(200)
        led.setColor(0, 50, 0)
        Tools.delay(200)

print("IdleProcess starting")
rc = 0
robot = Robot()
display = Display()
led = Led(LED_LEFT)
led.setColor(10, 10, 10) # Announce, we are starting
inCallback = False
robot.setButtonEnabled(False)
robot.addButtonListener(onButtonEvent, True)
isInterrupted = False
nbProg = getNbProg()
progID = 0
oldText = ""
ir_center = InfraredSensor(IR_CENTER)
if sys.argv[1] == "isFirst":
#    print "isFirst = True"
    firstDuty()
    if nbProg > 0:
        setConfigEntry("Programs", "LastProgram", "MyApp_1.py")
        progID = 1
else:
#    print "isFirst = False"
    robot.setButtonEnabled(True)
    pgm = getConfigEntry("Programs", "LastProgram")
#    print "last program:", pgm
    if pgm == None:
        progID = 0
    else:
        progID = int(pgm[6:7])

isAlive = True
led.setColor(0, 0, 50) # Announce, we are running

# Check if returning from execution of new downloaded file
file0 = SharedConstants.APP_PATH + ".py"
if os.path.isfile(file0) and int(os.path.getmtime(file0)) != 0: # file exists and time of modificaton not zero->update needed
   showUpdateInfo = False
else:
   showUpdateInfo = True
   showAppInfo(True)

isShutdownPending = False
while isAlive:
    updateAppFiles()
    startTime = time.time()
    while time.time() - startTime < 2 and isAlive:
        time.sleep(0.1)
display.clear()
if robot.oled != None:
    robot.oled.clear()
led.setColor(0, 0, 0)
Tools.delay(1000)
print("Returning to parent process with rc:", rc)
sys.exit(rc)




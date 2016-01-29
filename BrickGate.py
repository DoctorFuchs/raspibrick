# BrickGate.py

from raspibrick import *
from threading import Thread
import BrickGateProperties
import socket
import os, subprocess

def debug(msg):
    if BrickGateProperties.DEBUG:
        print "BG debug-> " + msg

# Response
class Error():
    OK = "0"
    SEND_FAILED = "-1"
    ILLEGAL_METHOD = "-2"
    ILLEGAL_INSTANCE = "-3"
    CMD_ERROR = "-4"
    CREATION_FAILED = "-5"

class Reply():
    OK = "OK"
    ILLEGAL_DEVICE = "ILLEGAL DEVICE"
    ILLEGAL_IDENTIFIER = "ILLEGAL IDENTIFIER"
    DEVICE_NOT_CREATED = "DEVICE NOT CREATED"
    ILLEGAL_COMMAND = "ILLEGAL COMMAND"
    METHOD_EVAL_FAILED = "METHOD EVAL FAILED"
    ILLEGAL_PARAMETER = "ILLEGAL PARAMETER"
    NO_SUCH_METHOD = "NO SUCH METHOD"
    CHAR_NOT_DISPLAYABLE = "CHAR NOT DISPLAYABLE"
    ILLEGAL_DECIMAL_POINT = "ILLEGAL DECIMAL POINT"
    ILLEGAL_DIGIT = "ILLEGAL DIGIT"
    IMAGE_CAPTURE_FAILED = "IMAGE CAPTURE FAILED"


# ---------------------- class JavaRunner ---------------------------
class JavaRunner(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.app = app
        self.start()

    def run(self):
        robot.isButtonHit()  # dummy call to reset buttonHit flag
        print "Spawning user app " + self.app
        rc = subprocess.call(["sudo", "java", "-jar", self.app])
        # return value not used yet
        print "Returning from MyApp with exit code:", rc

# ---------------------- class SocketHandler ------------------------
class SocketHandler(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        debug("SocketHandler started")
        global flasher
        global isConnected
        isRunning = True
        while isRunning:
            cmd = ""
            try:
                debug("Calling blocking conn.recv()")
                cmd = self.conn.recv(1024)[:-1]
            except:
                debug("exception in conn.recv()") # happens when connection is reset from the peer (Java Console closed)
                break
            debug("Received cmd: " + cmd + " len: " + str(len(cmd)))
            if len(cmd) == 0:
                break
            rc = self.executeCommand(cmd)
            if rc:
                isRunning = False
        conn.close()
        robot.exit()
        delay(2000)
        print "Client disconnected. Waiting for next client..."
        flasher = Flasher(led, [0, 100, 0])
        flasher.start()
        display.showText("HOLd")
        isConnected = False
        robot.setButtonEnabled(True)
        Tools.debug("SocketHandler terminated")

    def executeCommand(self, cmd):
        debug("Calling executeCommand() with  cmd: " + cmd)
        # max command length: device, method, param1, param2, param3, param4, param5
        reply = Reply.OK
        parts =  cmd.split(".")  # Split on period
        if len(parts) < 2 or len(parts) > 7:
            self.showError(Error.CMD_ERROR, cmd)
            self.sendReply(Reply.ILLEGAL_COMMAND)
            return
        if len(parts) == 2:
            parts.append("n")
            parts.append("n")
            parts.append("n")
            parts.append("n")
            parts.append("n")
        elif len(parts) == 3:
            parts.append("n")
            parts.append("n")
            parts.append("n")
            parts.append("n")
        elif len(parts) == 4:
            parts.append("n")
            parts.append("n")
            parts.append("n")
        elif len(parts) == 5:
            parts.append("n")
            parts.append("n")
        elif len(parts) == 6:
            parts.append("n")
        device = parts[0]
        method = parts[1]
        param1 = parts[2].replace("`", ".") # . is used as separator
        param2 = parts[3].replace("`", ".")
        param3 = parts[4].replace("`", ".")
        param4 = parts[5].replace("`", ".")
        param5 = parts[6].replace("`", ".")
        return self.dispatchCommand(device, method, param1, param2, param3, param4, param5)

    def dispatchCommand(self, device, method, param1, param2, param3, param4, param5):
        debug("dispatchCommand: " + device + ", " + method + ", " + param1 + ", " + param2 + \
              ", " + param3 + ", " + param4 + ", " + param5)
        reply = Reply.OK
        isExiting = False
        # ------------------- device 'robot'  ---------------
        if device == "robot":
            r = RobotInstance.getRobot()
            if method == "getVersion":
                reply = SharedConstants.VERSION
            elif method == "initSound":
                r.initSound(param1, int(param2))
            elif method == "playSound":
                r.playSound()
            elif method == "fadeoutSound":
                r.playSound(int(param1))
            elif method == "stopSound":
                r.stopSound()
            elif method == "pauseSound":
                r.pauseSound()
            elif method == "resumeSound":
                r.resumeSound()
            elif method == "rewindSound":
                r.rewindSound()
            elif method == "isSoundPlaying":
                if r.isSoundPlaying():
                    reply = "1"
                else:
                    reply = "0"
            elif method == "getIPAddresses":
                reply = ", ".join(r.getIPAddresses())
            elif method == "exit":
                isExiting = True
            elif method == "getCurrentDevices": # show all current devices in devices dictionary
                if len(devices) == 0:
                    reply = "NO DEVICES"
                else:
                    reply = ", ".join(devices.keys())
            elif method == "isButtonHit":
                if robot.isButtonHit():
                    reply = "1"
                else:
                    reply = "0"
            else:
                reply = Reply.NO_SUCH_METHOD

        # ------------------- device 'gear' or 'uss' ---------------
        elif device == "gear" or  device == "uss" or device == "cam":
            if method == "create":
                if not device in devices:
                    if device == "gear":
                        devices[device] = Gear()
                    elif device == "uss":
                        devices[device] = UltrasonicSensor()
                    elif device == "cam":
                        devices[device] = Camera()
                else:
                    pass # already created
            else:
                if not device in devices:
                    reply = Reply.DEVICE_NOT_CREATED
                else:
                    reply = evaluate(device, method, param1, param2, param3, param4, param5)

        elif device == "display":
            reply = dispatchDisplay(device, method, param1, param2, param3, param4, param5)

        # ------------------- static device 'led'  -----------
        elif device == "led":
            if method == "setColorAll":
                if param1 == "n" or param2 == "n" or param3 == "n":
                    reply = Reply.ILLEGAL_PARAMETER
                else:
                    try:
                        Led.setColorAll(int(param1), int(param2), int(param3))
                    except ValueError:
                        reply = Reply.ILLEGAL_PARAMETER
            elif method == "clearAll":
                Led.clearAll()
            else:
                reply = Reply.NO_SUCH_METHOD

        # ------------------- devices with identifier -----------
        elif len(device) > 3:
            devName = device[0:3]
            if devName == "mot" or  \
                devName == "irs" or   \
                devName == "led" or   \
                devName == "svo" or   \
                devName == "lss":
                try:
                    id = int(device[3:4])
                except ValueError:
                    reply = Reply.ILLEGAL_IDENTIFIER
                else:
                    if method == "create":
                        if not device in devices:
                            if devName == "mot":
                                devices[device] = Motor(id)
                            elif devName == "irs":
                                devices[device] = InfraredSensor(id)
                            elif devName == "led":
                                devices[device] = Led(id)
                            elif devName == "lss":
                                devices[device] = LightSensor(id)
                            elif devName == "svo":
                                devices[device] = ServoMotor(id,  int(param1), int(param2))
                        else:
                            pass # already created
                    else:
                        if not device in devices:
                            reply = Reply.DEVICE_NOT_CREATED
                        else:
                            reply = evaluate(device, method, param1, param2, param3, param4, param5)


        # ------------------- illegal device ----------------------------
        else:
            reply = Reply.ILLEGAL_DEVICE

        self.sendReply(reply)
        return isExiting

    def sendReply(self, reply):
        Tools.debug("Reply: " + reply)
        self.conn.sendall(reply + "\n")

    def sendImage(self, img):
        Tools.debug("Send Image size " + str(len(img)))
        self.conn.sendall(img)

    def showError(self, msg1, msg2):
        print "Error #" + msg1 + " : " + msg2
        display.showText("E" + msg1, [0, 1, 1])

def dispatchDisplay(device, method, param1, param2, param3, param4, param5):
    reply = "OK"
    if method == "create":
        if not device in devices:
            devices[device] = Display()
        else:
            pass # already created
    else:
        if not device in devices:
            reply = Reply.DEVICE_NOT_CREATED
        else:
            display = devices[device]
            if method == "clear":
                display.clear()
            elif method == "showText":
                if param2 == "n":
                    display.showText(param1)
                else:
                    stm = "display.showText(" + "\"" + param1 + "\", " + param2 + ", [" + param3 + "])"
                    debug("eval statement: " + stm)
                    eval(stm)
            elif method == "scrollToLeft":
                return str(display.scrollToLeft())
            elif method == "scrollToRight":
                return str(display.scrollToRight())
            elif method == "setToStart":
                display.setToStart()
            elif method == "stopTicker":
                display.stopTicker()
            elif method == "isTickerAlive":
                rc = display.isTickerAlive()
                if rc:
                    return "1"
                return "0"
            elif method == "isBlinkerAlive":
                rc = display.isBlinkerAlive()
                if rc:
                    return "1"
                return "0"
            elif method == "showTicker":
                if param4 == "0":
                    display.showTicker(param1, int(param2), int(param3), False)
                else:
                    display.showTicker(param1, int(param2), int(param3), True)
            elif method == "showBlinker":
                if param5 == "0":
                    stm = "display.showBlinker(" + "\"" + param1 + "\"" + ", [" + param2 + "], " + str(param3)  + ", " + str(param4) + ", False)"
                else:
                    stm = "display.showBlinker(" + "\"" + param1 + "\"" + ", [" + param2 + "], " + str(param3)  + ", " + str(param4) + ", True)"
                debug("eval statement: " + stm)
                eval(stm)
            else:
                reply = Reply.NO_SUCH_METHOD
    return reply

def evaluate(device, method, param1, param2, param3, param4, param5):
    dev = devices[device]  # Get device reference
    rc = None
    if param1 == "n":
        stm = "dev." + method + "()"
    elif param2 == "n":
        stm = "dev." + method + "(" + param1 + ")"
    elif param3 == "n":
        stm = "dev." + method + "(" + param1 + ", " + param2 + ")"
    elif param4 == "n":
        if method == "captureAndSave":
            param3 = "'" + param3 + "'"   # String parameter
        stm = "dev." + method + "(" + param1 + ", " + param2 + ", " + param3 + ")"
    elif param5 == "n":
        stm = "dev." + method + "(" + param1 + ", " + param2 + ", " + param3 + ", " + param4 + ")"
    else:
        if method == "startBlinker":
            param1 = "'" + param1 + "'"   # String parameter
            param2 = "'" + param2 + "'"   # String parameter
        stm = "dev." + method + "(" + param1 + ", " + param2 + ", " + param3 + ", " + param4 + ", " + param5 + ")"
    debug("Statement: " + stm)
    try:
        rc = eval(stm)
        debug("eval() returned: " +  str(rc))
    except:
        debug("eval() failed")
        return Reply.METHOD_EVAL_FAILED
    if rc == None:  # method with no return value
        return Reply.OK
    elif method == "captureJPEG" and rc == -1:
        return Reply.IMAGE_CAPTURE_FAILED
    else:
        return str(rc)  # convert return value to string

# ---------------------- Button callback ----------------------------
def onButtonEvent(event):
    global isLongPressed
    if not isButtonEnabled:
        return
    if event == BUTTON_PRESSED:
        isLongPressed = False
    elif event == BUTTON_LONGPRESSED:
        isLongPressed = True
        disconnect()
    elif event == BUTTON_RELEASED:
        if not isLongPressed:
            if isConnected:
                print "Button clicked while connected"
            else:
                javaApp = "/home/pi/programs/MyApp.jar"
                if os.path.isfile(javaApp):
                    javaRunner = JavaRunner(javaApp)
                else:
                    print "No Java app found to execute"
# ---------------------- class Flasher ------------------------------
class Flasher(Thread):
    def __init__(self, led, color):
        Thread.__init__(self)
        self.led = led
        self.color = color
        self.isFlashing = True

    def run(self):
        while self.isFlashing:
            self.led.setColor(self.color)
            Tools.delay(50)
            self.led.setColor(0, 0, 0)
            count = 0
            while count < 20 and self.isFlashing:
                count += 1
                Tools.delay(200)
        debug("FlasherThread terminated")

    def stop(self):
        self.isFlashing = False

    def setColor(self, color):
        self.color = color

def blinkRed(led, nb):
    for n in range(nb):
        led.setColor(255, 0, 0)
        Tools.delay(100)
        led.setColor(0, 0, 0)
        Tools.delay(200)

def delay(interval):
    time.sleep(interval / 1000.0)

def toBin(n):
    a = [n & 4 != 0, n & 2 != 0, n & 1 != 0]
    for i in range(3):
        if a[i]:
            a[i] = 1
        else:
            a[i] = 0
    return a

def disconnect():
    global terminateServer
    terminateServer = True
    debug("Dummy connection...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', BrickGateProperties.IP_PORT))  # dummy connection to get out of accept()


# ====================== Main ======================================
print "Brickgate server V" + BrickGateProperties.BRICKGATE_VERSION + " starting"
isButtonEnabled = False
SharedConstants.BLINK_CONNECT_DISCONNECT = False
SharedConstants.PLAY_CONNECT_DISCONNECT = False
robot = Robot()
Led.clearAll()
led = Led(LED_LEFT)
flasher = Flasher(led, [0, 100, 0])
display = Display()
Tools.delay(3000)
isConnected = False
robot.addButtonListener(onButtonEvent)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # close port when process exits
Tools.debug("Socket created")

# dictionary of devices: "device_tag":ref
devices = {}

HOSTNAME = "" # Symbolic name meaning all available interfaces
try:
    serverSocket.bind((HOSTNAME, BrickGateProperties.IP_PORT))
except socket.error as msg:
    print "Bind failed", msg[0], msg[1]
    sys.exit()
serverSocket.listen(10)
terminateServer = False
display.showText("HOLd")
flasher.start()
isButtonEnabled = True
print "Waiting for a connecting client..."
while True:
    # wait to accept a connection - blocking call
    Tools.debug("Calling blocking accept()...")
    conn, addr = serverSocket.accept()
    print "Connected with client at " + addr[0]
    if terminateServer:
        break
    if isConnected:  # Accept only one connection
        continue
    flasher.stop()
    display.showText("Conn")
    Tools.delay(1500)
    display.clear()
    isConnected = True
    devices.clear()
    socketHandler = SocketHandler(conn)
    socketHandler.setDaemon(True)  # necessary to terminate it at program termination
    socketHandler.start()
display.clear()
flasher.stop()
blinkRed(led, 2)
serverSocket.close()
print "BrickGate terminated"


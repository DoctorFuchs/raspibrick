# Display.py
# Inspired from ipd03.py from 4tronix, with thanks to the author
'''
The 7 segments have the following binary values
           1
           -
     32 |     |2

          64
           -
     16 |     |4
           -
           8

The decimal points use value 128 with digit 1, 2 or 3
'''

import smbus
import RPi.GPIO as GPIO
from RobotInstance import RobotInstance
from Tools import *
from threading import Thread

def delay(interval):
    time.sleep(interval / 1000.0)

# I2C address of MCP23017
_addr = 0x20

class TickerThread(Thread):
    def __init__(self, display, text, count, speed):
        Thread.__init__(self)
        self._text = text
        self._display = display
        if speed <= 0:
            speed = 1
        self._period = int(1000.0 / speed)
        self._count = count
        self._isRunning = False
        self._isAlive = True
        self.start()
        while not self._isRunning:
            continue

    def run(self):
        Tools.debug("TickerThread started")
        self._display.setScrollableText(self._text)
        nb = 0
        self._isRunning = True
        while self._isRunning:
            startTime = time.clock()
            while time.clock() - startTime < self._period / 10000.0 and self._isRunning:
                Tools.delay(1)
            if not self._isRunning:
                break
            rc = self._display.scrollToLeft()
            if rc == 4 and self._isRunning:
                startTime = time.clock()
                while time.clock() - startTime < 0.5 and self._isRunning:
                    Tools.delay(10)
                if not self._isRunning:
                    break
                nb += 1
                if nb == self._count:
                    break
                self._display.setToStart()
        if self._isRunning:
            while time.clock() - startTime < 0.5 and self._isRunning:
                Tools.delay(10)
            self._display._bus.write_byte_data(_addr, 0x13, 0xff) # Clear
        Tools.debug("TickerThread terminated")
        self._isAlive = False

    def stop(self):
        self._isRunning = False
        while self._isAlive:
            continue
        Tools.debug("Clearing display")
        self._display.clear()

class DisplayThread(Thread):
    def __init__(self, display):
        Thread.__init__(self)
        self._display = display

    def run(self):
        Tools.debug("DisplayThread started")
        self._isAlive = True
        self._isRunning = True
        while self._isRunning:
            delays = 0
            for digit in range(4):
                self._display.setDigit(self._display._text[digit], digit)
                delay(2)
                delays += 1
                self._display.clearDigit(digit)
                if not self._isRunning:
                    break
            if 1 in self._display._decimalPoint:
                for i in range(3):
                    if self._display._decimalPoint[i] == 1:
                        self._display.setDecimalPoint(i)
                        delay(2)
                        delays += 1
                        self._display.clearDigit(2-i)
                        if not self._isRunning:
                            break
        self.isAlive = False
        Tools.debug("DisplayThread finished")

    def stop(self):
        self._isRunning = False
        while self.isAlive:
            continue

# ------------------------   Class Display  -------------------------------------------
class Display():
    '''
    Abstraction of the 4 digit 7-segment display attached to the I2C port.
    If no display is found, all methods return immediately. Be aware that the display
    is multiplexed by an internal display thread. So while a text is displayed the thread is
    running and the program will not terminate. Call clear() to terminate the display thread.
    '''
    _myInstance = None
    def __init__(self):
        self._checkRobot()
        robot = RobotInstance.getRobot()
        self.available = robot._isDisplayAvailable
        if not self.available:
            return
        self._bus = robot._bus
        self._displayThread = None
        self._text = [' '] * 4
        self._decimalPoint = [0] * 3
        self._tickerThread = None
        Display._myInstance = self

    def setDigit(self, char, digit):
        '''
        Shows the given character at one of the 4 7-segment digits. The character is mapped to
        its binary value using the PATTERN dictionary define in SharedConstants.py.
        Only one digit can be used at the same time. This method has much less overhead than calling
        setValue(), because no internal display thread is started. The display remains active even when the program
        terminates.
        @param char: the character to display
        @param digit: the display ID (0 is leftmost, 3 is rightmost)
        @return: True, if successful; False, if the character is not displayable
            or digit not in 0..3  or display not available
        '''
        if not self.available:
            return False
        self._checkRobot()
        if digit < 0 or digit > 3:
            return False
        try:
            if type(char) == int:
                v = SharedConstants.PATTERN[str(char)]
            else:
                v = SharedConstants.PATTERN[char]
        except:
            print "Can't display", char
            return False
        return self.setBinary(v, digit)

    def setBinary(self, value, digit):
        '''
        Shows the pattern of the binary value 0..255.
        @param value: the byte value
        @param digit: the display ID (0 is leftmost, 3 is rightmost)
        @return: True, if successful; False, if value not in 0..255 or digit not in 0..3 or display not available
        '''
        if not self.available:
            return False
        self._checkRobot()
        if value < 0 or value > 255:
            return False
        if digit < 0 or digit > 3:
            return False
        t = (1 << (3 - digit)) ^ 255
        self._bus.write_byte_data(_addr, 0x13, t) # Set bank 1 pos to low
        self._bus.write_byte_data(_addr, 0x12, value) # Set bank 0 to digit
        return True

    def setDecimalPoint(self, id):
        '''
        Shows one of the 3 decimal points.
        @param id: select the DP to show: 0: right bottom, 1: middle bottom, 2: middle top
        @return: True, if successful; False, if id not in 0..2 or display not available
        '''
        if not self.available:
            return False
        if id < 0 or id > 2:
            return False
        self.setBinary(128, 2 - id)
        return True

    def clearDigit(self, digit):
        '''
        Clears the given digit.
        @param digit: the display ID (0 is right most, 3 is left most)
        @return: True, if successful; False, if digit not in 0..3 or display not available
        '''
        if not self.available:
            return False
        if digit < 0 or digit > 3:
            return False
        self.setDigit(' ', digit)
        return True

    def clear(self):
        '''
        Turns all digits off. Stops a running display thread.
        '''
        if not self.available:
            return
        self._checkRobot()
        if self._displayThread != None:
            self._displayThread.stop()
            self._displayThread = None
        self._bus.write_byte_data(_addr, 0x13, 0xff) # Set all of bank 1 to high (all digits off)

    def setText(self, text, dp = [0, 0, 0]):
        '''
        Displays the given text right justified using an display thread. If the text to display exceeds 4 digits,
        only the 4 leading digits are shown. Because only one digit can be used at the same time,
        an internal display thread is created that drives the digits repeatedly in a fast sequence.
        Call clear() to stop the thread when it is no longer used. To display decimal points, use the
        dp paramater [right bottom, middle bottom, middle top] and set the decimal point values to 1
        @param text: the text to display (list, string or integer)
        @param dp: a list with three 1 or 0, if the decimal point is shown or not
        '''
        if not self.available:
            return
        self._checkRobot()
        if not (type(text) == int or type(text) == list or type(text) == str):
            return
        self._decimalPoint = dp
        self._text = [' '] * 4  # blanks
        if type(text) == int:
            text = str(text)
        text = text[0:4]
        offset = 4 - len(text)
        for i in range(len(text)):
            self._text[i + offset] = text[i]
        if self._displayThread == None:
            self._displayThread = DisplayThread(self)
            self._displayThread.start()

    def setScrollableText(self, text, pos = 0):
        '''
        Displays a text that can be scrolled. A text position index is used that
        determines the character displayed at leftmost digit. Default pos = 0
        @param text: the text displayed
        @param pos: the start value of the text pointer (character index positioned a leftmost digit)
        '''
        if not self.available:
            return
        self._checkRobot()
        self._scrollText = text
        self._startPos = pos
        self._pos = pos
        self.setText(text[pos:], [0, 0, 0])

    def scrollToLeft(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the right
        '''
        if not self.available:
            return
        self._checkRobot()
        self._pos += 1
        text = self._scrollText[self._pos:]
        self.setText(text)
        return len(text)

    def scrollToRight(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the left
        '''
        if not self.available:
            return
        self._checkRobot()
        self._pos -= 1
        text = self._scrollText[self._pos:]
        self.setText(text)
        return len(self._scrollText) - len(text)

    def setToStart(self):
        '''
        Shows the scrollable text at the start position.
        '''
        if not self.available:
            return
        self._checkRobot()
        self._pos = self._startPos
        text = self._scrollText[self._pos:]
        self.setText(text)
        return len(text)

    def ticker(self, text, count = 1, speed = 2, blocking = False):
        '''
        Shows a ticker text that scroll to left until the last 4 characters are displayed. The method blocks
        until the ticker thread is successfully started and isTickerAlive() returns True.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 1). For count == 0, infinite duration,
        may be stopped by calling stopTicker().
        @param speed: the speed number of scrolling operations per sec (default: 2)
        @param blocking: if True, the method blocks until the ticker has finished; otherwise
         it returns immediately (default: False)
        '''
        if not self.available:
            return
        self._checkRobot()
        self.clear();
        if self._tickerThread != None:
            self.stopTicker()
        self._tickerThread = TickerThread(self, text, count, speed)
        if blocking:
            self._tickerThread.join()

    def stopTicker(self):
        '''
        Stops a running ticker.
        The method blocks until the ticker thread is finished and isTickerAlive() returns False.
        '''
        if not self.available:
            return
        self._checkRobot()
        if self._tickerThread != None:
            self._tickerThread.stop()
            self._tickerThread = None

    def isTickerAlive(self):
        '''
        @return: True, if the ticker is displaying; otherwise False
        '''
        if not self.available:
            return True
        Tools.delay(1)
        self._checkRobot()
        if self._tickerThread == None:
            return False
        return self._tickerThread._isAlive

    def getDisplayableChars(self):
        '''
        Returns a string with all displayable characters.
        @return: The character set that can be displayed
        '''
        s = ""
        for key in SharedConstants.PATTERN:
            if key != " ":
               s = s + key
        return  "".join(sorted(s)) + "<SPACE>"

    def isAvailable(self):
        '''
        @return: True, if the display is detetectd on the I2C interface; otherwise False
        '''
        return self.available

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

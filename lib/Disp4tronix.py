# Disp4tronix.py
# Inspired from ipd03.py from 4tronix, with thanks to the author

'''
Class that represents a 7-segment display from 4tronix attached to the I2C port.

 
 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code777
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.


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

The digigs are multiplexed (refreshed one after the other). So some flickering
may happen when the CPU is highly loaded.
'''

from smbus import *
import RPi.GPIO as GPIO
from Tools import *
from threading import Thread

# ------------------------   Class Display  -------------------------------------------
class Disp4tronix():
    '''
    Abstraction of the 4 digit 7-segment display from 4tronix attached to the I2C port.
    If no display is found, all methods return immediately. Be aware that the display
    is multiplexed by an internal display thread. So while a text is displayed the thread is
    running and the program will not terminate. Call clear() to terminate the display thread.
    '''
    DEBUG = False
    VERSION = "1.00"
    i2c_address = 0x20
    _myInstance = None

    '''pi

    Character to binary value mapping for 4 digit 7 segment display
    '''
    PATTERN = {' ': 0, '!': 134, '"': 34, '#': 0, '$': 0, '%': 0, '&': 0, '\'':  2, '(': 0, ')': 0,
           '*': 0, '+': 0, ',': 4, '-': 64, '.': 128, '/': 82, '0': 63, '1': 6, '2': 91, '3': 79,
           '4': 102, '5': 109, '6': 125, '7': 7, '8': 127, '9': 111, ':': 0, ';': 0, '<': 0,
           '=': 72, '>': 0, '?': 0, '@': 93, 'A': 119, 'B': 124, 'C': 57, 'D': 94, 'E': 121,
           'F': 113, 'G': 61, 'H': 118, 'I': 48, 'J': 14, 'K': 112, 'L': 56, 'M': 85, 'N': 84,
           'O': 63, 'P': 115, 'Q': 103, 'R': 80, 'S': 45, 'T': 120, 'U': 62, 'V': 54, 'W': 106,
           'X': 73, 'Y': 110, 'Z': 27, '[': 57, '\\':  100, ']': 15, '^': 35, '_': 8, '`': 32,
           'a': 119, 'b': 124, 'c': 88, 'd': 94, 'e': 121, 'f': 113, 'g': 61, 'h': 116, 'i': 16,
           'j': 12, 'k': 112, 'l': 48, 'm': 85, 'n': 84, 'o': 92, 'p': 115, 'q': 103, 'r': 80, 's': 45,
           't': 120, 'u': 28, 'v': 54, 'w': 106, 'x': 73, 'y': 110, 'z': 27, '{': 0, '|': 48, '}': 0, '~': 65}

# -------------------- Static methods ---------------------
    @staticmethod
    def toHex(intValue):
        '''
        Returns a string with hex digits from given number (>0, any size).
        @param number: the number to convert (must be positive)
        @return: string of hex digits (uppercase), e.g. 0xFE
        '''
        return '%02x' % intValue

    @staticmethod
    def toBytes(intValue):
        '''
        Returns a list of four byte values [byte#24-#31, byte#16-#23, byte#8-#15, byte#0-#7] of given integer.
        @param number: an integer
        @return: list with integers of 4 bytes [MSB,..., LSB]
        '''
        byte0 = intValue & 0xff
        byte1 = (intValue >> 8) & 0xff
        byte2 = (intValue >> 16) & 0xff
        byte3 = (intValue >> 24) & 0xff
        return [byte3, byte2, byte1, byte0]

    @staticmethod
    def toInt(hexValue):
        '''
        Returns an integer from given hex string
        @param number: a string with the number to convert, e.g. "FE" or "fe" or "0xFE" or "0XFE"
        @return: integer number
        '''
        return int(hexValue, 16)

    @staticmethod
    def debug(msg):
        if Disp4tronix.DEBUG:
            print "Disp4tronix debug->", msg

    @staticmethod
    def getVersion():
        return Disp4tronix.VERSION

    @staticmethod
    def getDisplayableChars():
        '''
        Returns a string with all displayable characters taken from PATTERN dictionary.
        @return: The character set that can be displayed
        '''
        s = "<SPACE>"
        k = 33
        while k < 127:
            ch = chr(k)
            if Disp4tronix.PATTERN[ch] != 0:
                s = s + ch
            k += 1
        return  s

    @staticmethod
    def delay(interval):
        time.sleep(interval / 1000.0)

    # -------------------- Ctor --------------------------------
    def __init__(self):
        self._bus = None
        self._displayThread = None
        self._tickerThread = None
        self._blinkerThread = None
        try:
            if GPIO.RPI_REVISION > 1:
                self._bus = SMBus(1) # For revision 2 Raspberry Pi
                Disp4tronix.debug("I2C at bus 1 detected")
            else:
                self._bus = SMBus(0) # For revision 1 Raspberry Pi
                Disp4tronix.debug("I2C at bus 0 detected")
        except:
            Disp4tronix.debug("Failed to detect I2C bus.")

        if self._bus != None:
            self._bus.write_byte_data(Disp4tronix.i2c_address, 0x00, 0x00) # Set all of bank 0 to outputs
            self._bus.write_byte_data(Disp4tronix.i2c_address, 0x01, 0x00) # Set all of bank 1 to outputs
            self._bus.write_byte_data(Disp4tronix.i2c_address, 0x13, 0xff) # Set all of bank 1 to high (all digits off)
            self._startPos = -1  # no text yet
        Disp4tronix._myInstance = self
        Disp4tronix.debug("Disp4tronix instance created")

    def setDigit(self, char, digit):
        '''
        Shows the given character at one of the 4 7-segment digits. The character is mapped to
        its binary value using the PATTERN dictionary defined in PATTERN dictonary.
        Only one digit can be used at the same time. This method has much less overhead than calling
        setValue(), because no internal display thread is started. The display remains active even when the program
        terminates.
        @param char: the character to display, can be an int 0..9
        @param digit: the display ID (0 is leftmost, 3 is rightmost)
        @return: True, if successful; False, if the character is not displayable
            or digit not in 0..3
        '''
        if self._bus == None:
            return False
        if digit < 0 or digit > 3:
            return False
        try:
            if type(char) == int:
                v = Disp4tronix.PATTERN[str(char)]
            else:
                v = Disp4tronix.PATTERN[char]
        except:
            v = 0
        return self.setBinary(v, digit)

    def setBinary(self, value, digit):
        '''
        Shows the pattern of the binary value 0..255.
        @param value: the byte value
        @param digit: the display ID (0 is leftmost, 3 is rightmost)
        @return: True, if successful; False, if value not in 0..255 or digit not in 0..3
        '''
        if self._bus == None:
            return False
        if value < 0 or value > 255:
            return False
        if digit < 0 or digit > 3:
            return False
        t = (1 << (3 - digit)) ^ 255
        self._bus.write_byte_data(Disp4tronix.i2c_address, 0x13, t) # Set bank 1 pos to low
        self._bus.write_byte_data(Disp4tronix.i2c_address, 0x12, value) # Set bank 0 to digit
        return True

    def setDecimalPoint(self, id):
        '''
        Shows one of the 3 decimal points.
        @param id: select the DP to show: 0: right bottom, 1: middle bottom, 2: middle top
        @return: True, if successful; False, if id not in 0..2
        '''
        if self._bus == None:
            return False
        if id < 0 or id > 2:
            return False
        self.setBinary(128, 2 - id)
        return True

    def clearDigit(self, digit):
        '''
        Clears the given digit.
        @param digit: the display ID (0 is right most, 3 is left most)
        @return: True, if successful; False, if digit not in 0..3
        '''
        if self._bus == None:
            return False
        if digit < 0 or digit > 3:
            return False
        self.setDigit(' ', digit)
        return True

    def clear(self):
        '''
        Turns all digits off. Stops a running display thread. To clear all digits
        without terminating the display thread, call showText("    ").
        '''
        if self._bus == None:
            return
        if self._displayThread != None:
            self._displayThread.stop()
            self._displayThread = None
        self._bus.write_byte_data(Disp4tronix.i2c_address, 0x13, 0xff) # Set all of bank 1 to high (all digits off)

    def showText(self, text, pos = 0, dp = [0, 0, 0]):
        '''
        Displays 4 characters of the given text. The text is considered to be prefixed and postfixed by spaces
        and the 4 character window is selected by the text pointer pos that determines the character displayed at the
        leftmost digit, e.g. (_: empty):
        showText("AbCdEF") -> AbCd
        showText("AbCdEF", 1) -> bCdE
        showText("AbCdEF", -1) ->_AbC
        showText("AbCdEF", 4) -> EF__
        To display a character and its decimal point, use the dp parameter [most right dp,...,most left dp] and
        set the decimal point values to 1. If the display thread is not yet running,
        it is started now.
        @param text: the text to display (list, tuple, string or integer)
        @param pos: the start value of the text pointer (character index positioned a leftmost digit)
        @param dp: a list with one to three 1 or 0, if the decimal point is shown or not. First element in list
        corresponds to right dp, second to center floor dp, third to center ceil dp. More than 3 elements are
        ignored
        arbitrary
        @return: True, if successful; False, if the display is not available,
        text or dp has illegal type or one of the characters can't be displayed
        '''
        Disp4tronix.debug("showText(" + str(text) + "," + str(pos) + "," + str(dp) + ")")
        if self._bus == None:
            return False
        if not (type(text) == int or type(text) == list or type(text) == tuple or type(text) == str):
            return False
        if not (type(dp) == list or type(dp) == tuple):
            return False
        self._startPos = pos
        self._pos = pos
        self._decimalPoint = [0] * 3
        for i in range(len(dp)):
            if i < 3:
                self._decimalPoint[i] = dp[i]
        self._text = str(text)  # convert digits to chars
        self._data = self._getData(self._pos)
        if self._displayThread == None:
            self._displayThread = DisplayThread(self)
            self._displayThread.start()
            while not self._displayThread._isAlive:
                Tools.delay(10)
        return True

    def scrollToLeft(self):
        '''
        Scrolls the current text one step to the left by increasing the text pointer.
        @return: the number of characters hidden, but remaining to be displayed at the right (>=0); -1, if error
        '''
        if self._bus == None:
            return -1
        if self._startPos == -1:  # no text yet
            return -1
        self._pos += 1
        self._data = self._getData(self._pos)
        nb = len(self._text) - self._pos
        return max(0, nb)

    def scrollToRight(self):
        '''
        Scrolls the current text one step to the left by decreasing the text pointer.
        @return: the number of characters hidden, but remaining to be displayed at the left (>=0); -1, if error
        '''
        if self._bus == None:
            return -1
        if self._startPos == -1:  # no text yet
            return -1
        self._pos -= 1
        pos = self._pos
        self._data = self._getData(self._pos)
        nb = len(self._text) - self._pos
        return max(0, self._pos)

    def setToStart(self):
        '''
        Shows the scrollable text at the start position by setting the text pointer to its start value.
        @return: 0, if successful; -1, if error
        '''
        if self._bus == None:
            return -1
        if self._startPos == -1:  # no text yet
            return -1
        self._pos = self._startPos
        self._data = self._getData(self._pos)
        nb = len(self._text) - self._pos
        return 0

    def showTicker(self, text, count = 1, speed = 2, blocking = False):
        '''
        Shows a ticker text that scroll to left until the last 4 characters are displayed. The method blocks
        until the ticker thread is successfully started and isTickerAlive() returns True.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 1). For count = 0, infinite duration,
        may be stopped by calling stopTicker().
        @param speed: the speed number of scrolling operations per sec (default: 2)
        @param blocking: if True, the method blocks until the ticker has finished; otherwise
         it returns immediately (default: False)
        '''
        if self._bus == None:
            return
        self.clear();
        if self._tickerThread != None:
            self.stopTicker()
        self._tickerThread = TickerThread(self, text, count, speed)
        if blocking:
            while self.isTickerAlive():
                continue

    def stopTicker(self):
        '''
        Stops a running ticker.
        The method blocks until the ticker thread is finished and isTickerAlive() returns False.
        '''
        if self._bus == None:
            return
        if self._tickerThread != None:
            self._tickerThread.stop()
            self._tickerThread = None

    def isTickerAlive(self):
        '''
        @return: True, if the ticker is displaying; otherwise False
        '''
        if self._bus == None:
            return
        Tools.delay(1)
        if self._tickerThread == None:
            return False
        return self._tickerThread._isAlive

    def showBlinker(self, text, dp = [0, 0, 0, 0], count = 3, speed = 1, blocking = False):
        '''
        Shows a ticker text that scroll to the left until the last 4 characters are displayed. The method blocks
        until the ticker thread is successfully started and isTickerAlive() returns True.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 2). For count = 0, infinite duration,
        may be stopped by calling stopBlinker().
        @param speed: the speed number of blinking operations per sec (default: 1)
        @param blocking: if True, the method blocks until the blinker has finished; otherwise
         it returns immediately (default: False)
        '''
        if self._bus == None:
            return
        self.clear();
        if self._tickerThread != None:
            self.stopTicker()
        if self._blinkerThread != None:
            self.stopBlinker()
        self._blinkerThread = BlinkerThread(self, text, dp, count, speed)
        if blocking:
            while self.isBlinkerAlive():
                continue

    def stopBlinker(self):
        '''
        Stops a running blinker.
        The method blocks until the blinker thread is finished and isBlinkerAlive() returns False.
        '''
        if self._bus == None:
            return
        if self._blinerThread != None:
            self._blinkerThread.stop()
            self._blinkerThread = None

    def isBlinkerAlive(self):
        '''
        @return: True, if the blinker is displaying; otherwise False
        '''
        if self._bus == None:
            return False
        Disp4tronix.delay(1)
        if self._blinkerThread == None:
            return False
        return self._blinkerThread._isAlive

    def showVersion(self):
        '''
        Displays current version. Format X (three horz bars) + n.nn
        '''
        v = "X" + Disp4tronix.VERSION.replace(".", "")
        self.showText(v, pos = 0, dp = [0, 1])

    def isAvailable(self):
        if self._bus != None:
            return True
        return False

    # -------------------- private methods ----------------------------
    def _getData(self, pos):
        li = [0] * len(self._text)
        for i in range(len(li)):
            li[i] = self._text[i]
        if pos >= 0:
            data = li[pos:pos + 4]
            for i in range(4 - len(data)):
                data.append(' ') # spaces
        else:
            if 4 + pos >= 0:
                data = li[0:4 + pos]
            else:
                data = []
            data.reverse()
            for i in range(4 - len(data)):
                data.append(' ') # spaces
            data.reverse()
        r = ''.join(data)
        return r


# --------------- class DisplayThread ----------------
class DisplayThread(Thread):
    def __init__(self, display):
        Thread.__init__(self)
        self._display = display
        self._isRunning = False
        self._isAlive = False

    def run(self):
        Disp4tronix.debug("DisplayThread started")
        self._isAlive = True
        self._isRunning = True
        while self._isRunning:
            delays = 0
            for digit in range(4):
                self._display.setDigit(self._display._data[digit], digit)
                Disp4tronix.delay(2)
                delays += 1
                self._display.clearDigit(digit)
                if not self._isRunning:
                    break
            if 1 in self._display._decimalPoint:
                for i in range(3):
                    if self._display._decimalPoint[i] == 1:
                        self._display.setDecimalPoint(i)
                        Disp4tronix.delay(2)
                        delays += 1
                        self._display.clearDigit(2-i)
                        if not self._isRunning:
                            break
        self._isAlive = False
        self._isRunning = False
        Disp4tronix.debug("DisplayThread terminated")

    def stop(self):
        self._isRunning = False
        while self._isAlive:
            continue

# --------------- class TickerThread ----------------
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
        Disp4tronix.debug("TickerThread started")
        self._display.showText(self._text)
        nb = 0
        self._isRunning = True
        while self._isRunning:
            startTime = time.time()
            while time.time() - startTime < self._period / 1000.0 and self._isRunning:
                Disp4tronix.delay(10)
            if not self._isRunning:
                break
            rc = self._display.scrollToLeft()
            if rc == 4 and self._isRunning:
                startTime = time.time()
                while time.time() - startTime < 2 and self._isRunning:
                    Disp4tronix.delay(10)
                if not self._isRunning:
                    break
                nb += 1
                if nb == self._count:
                    break
                self._display.setToStart()
        if self._isRunning:  # terminated by number of count
            while time.time() - startTime < 2 and self._isRunning:
                Disp4tronix.delay(10)
            self._display.clear()
        Disp4tronix.debug("TickerThread terminated")
        self._isAlive = False

    def stop(self):
        self._isRunning = False
        while self._isAlive: # Wait until thread is finished
            continue
        Tools.debug("Clearing display")
        self._display.clear()

# ------------------- class BlinkerThread ----------------------
class BlinkerThread(Thread):
    def __init__(self, display, text, dp, count, speed):
        Thread.__init__(self)
        self._text = text
        self._dp = dp
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
        Disp4tronix.debug("BlinkerThread started")
        nb = 0
        self._isRunning = True
        while self._isRunning:
            self._display.showText(self._text, dp = self._dp)
            startTime = time.time()
            while time.time() - startTime < self._period / 1000.0 and self._isRunning:
                Disp4tronix.delay(1)
            if self._isRunning == False:
                break
            self._display.showText("    ", dp = [0, 0, 0])
            startTime = time.time()
            while time.time() - startTime < self._period / 1000.0 and self._isRunning:
                Disp4tronix.delay(1)
            if self._isRunning == False:
                break
            nb += 1
            if nb == self._count:
                self._isRunning = False

        startTime = time.time()
        while time.time() - startTime < 1:
            Disp4tronix.delay(1)
        self._display.clear() # Terminate display thread
        Disp4tronix.debug("BlinkerThread terminated")
        self._isAlive = False

    def stop(self):
        self._isRunning = False
        while self._isAlive: # Wait until thread is finished
            continue

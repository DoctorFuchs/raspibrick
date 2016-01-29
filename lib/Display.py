# Display.py

'''
Class that represents a 7-segment display attached to the I2C port.

 
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
'''

from Disp4tronix import Disp4tronix
from DgTell import DgTell
from DgTell1 import DgTell1
from RobotInstance import RobotInstance
from Tools import *

# ------------------------   Class Display  -------------------------------------------
class Display():
    '''
    Abstraction of the 4 digit 7-segment display attached to the I2C port.
    If no display is found, all methods return immediately.
    '''
    _myInstance = None

    def __init__(self):
        '''
        Creates a display instance either from class Display4tronix or DisplayDidel.
        Because the 4tronix display is multiplexed (one digit shown after
        the other, a display thread is used to display all 4 digits in a rapid succession.
        '''
        self._checkRobot()
        robot = RobotInstance.getRobot()
        self.text = ""
        self.pos = 0
        self.dp = [0, 0, 0, 0]
        if robot.displayType == "4tronix":
            Display._myInstance = Disp4tronix()
            self.available = True
        elif robot.displayType == "didel":
            Display._myInstance = DgTell()
            self.available = True
        elif robot.displayType == "didel1":
            Display._myInstance = DgTell1()
            self.available = True
        else:
            self.available = False


    def clear(self):
        '''
        Turns all digits off. Stops a running display thread.
        '''
        if not self.available:
            return
        self._checkRobot()
        return Display._myInstance.clear()

    def showText(self, text, pos = 0, dp = [0, 0, 0, 0]):
        '''
        Displays 4 characters of the given text. The text is considered to be prefixed and postfixed by spaces
        and the 4 character window is selected by the text pointer pos that determines the character displayed at the
        leftmost digit, e.g. (_: empty):
        showText("AbCdEF") -> AbCd
        showText("AbCdEF", 1) -> bCdE
        showText("AbCdEF", -1) ->_AbC
        showText("AbCdEF", 4) -> EF__
        Because the 4tronix display is multiplexed (one digit shown after the other),
        a display thread is started now to display all 4 digits in a rapid succession (if it is not yet started).
        The parameters are saved and compared to the values at the next invocation. If all are identical, the function returns
        immediately.
        @param text: the text to display (list, tuple, string or integer)
        @param pos: the start value of the text pointer (character index positioned a leftmost digit)
        @param dp: a list with one to four 1 or 0, if the decimal point is shown or not.
        The decimal point selection depends on the attached display type. For the 4tronix display: the first element in list
        corresponds to right dp, second element to center floor dp, the third element to center ceil dp. For the DgTell:
        the first element in list corresponds to dp at second digit from the right, the second element to dp
        at third digit from the right, the third element to dp at leftmost digit, the forth element to the dp at
        rightmost digit.  More than 4 elements are ignored
        @return: True, if successful; False, if the display is not available,
        text or dp has illegal type or one of the characters can't be displayed
        '''
        if not self.available:
            return
        if text == self.text and pos == self.pos and cmp(dp, self.dp) == 0:
            return
        self.text = text
        self.pos = pos
        self.dp = dp
        self._checkRobot()
        if type(pos) != int:
            pos = 0
        if type(dp) != list:
            dp = [0, 0, 0, 0]
        Display._myInstance.showText(text, pos, dp)

    def scrollToLeft(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the right
        '''
        if not self.available:
            return
        self._checkRobot()
        return Display._myInstance.scrollToLeft()

    def scrollToRight(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the left
        '''
        if not self.available:
            return
        return Display._myInstance.scrollToRight()

    def setToStart(self):
        '''
        Shows the scrollable text at the start position.
        @return: 0, if successful; -1, if error
        '''
        if not self.available:
            return
        self._checkRobot()
        return Display._myInstance.setToStart()

    def showTicker(self, text, count = 1, speed = 2, blocking = False):
        '''
        Shows a ticker text that scroll to left until the last 4 characters are displayed.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 1). For count = 0, infinite duration,
        may be stopped by calling stopTicker().
        @param speed: the speed number of scrolling operations per sec (default: 2)
        @param blocking: if True, the method blocks until the ticker has finished; otherwise
         it returns immediately (default: False)
        '''
        if not self.available:
            return
        self._checkRobot()
        Display._myInstance.showTicker(text, count, speed, blocking)

    def stopTicker(self):
        '''
        Stops a running ticker.
        The method blocks until the ticker thread is finished and isTickerAlive() returns False.
        '''
        if not self.available:
            return
        self._checkRobot()
        Display._myInstance.stopTicker()

    def isTickerAlive(self):
        '''
        @return: True, if the ticker is displaying; otherwise False
        '''
        if not self.available:
            return False
        Tools.delay(1)
        self._checkRobot()
        return Display._myInstance.isTickerAlive()

    def showBlinker(self, text, dp = [0, 0, 0, 0], count = 3, speed = 1, blocking = False):
        '''
        Shows a blinking text for the given number of times and blinking speed.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 3). For count = 0, infinite duration,
        may be stopped by calling stopBlinker().
        @param speed: the speed number of blinking operations per sec (default: 1)
        @param blocking: if True, the method blocks until the blinker has finished; otherwise
         it returns immediately (default: False)
        '''
        if not self.available:
            return
        self._checkRobot()
        Display._myInstance.showBlinker(text, dp, count, speed, blocking)

    def stopBlinker(self):
        '''
        Stops a running blinker.
        The method blocks until the blinker thread is finished and isBlinkerAlive() returns False.
        '''
        if not self.available:
            return
        self._checkRobot()
        Display._myInstance.stopBlinker()

    def isBlinkerAlive(self):
        '''
        @return: True, if the blinker is displaying; otherwise False
        '''
        if not self.available:
            return False
        Tools.delay(1)
        self._checkRobot()
        return Display._myInstance.isBlinkerAlive()

    def showVersion(self):
        '''
        Displays current version. Format X (three horz bars) + n.nn
        '''
        v = "X" + DgTell.VERSION.replace(".", "")
        self.showText(v, pos = 0, dp = [0, 1])

    def isAvailable(self):
        '''
        @return: True, if the display is detetectd on the I2C interface; otherwise False
        '''
        if not self.available:
            return False
        return self.available

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")



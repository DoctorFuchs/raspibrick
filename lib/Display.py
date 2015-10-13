# Display.py
# Remote mode
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

from RobotInstance import RobotInstance


# ------------------------   Class Display  -------------------------------------------
class Display():

    def __init__(self):
        self.device = "display"
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create")
        self.robot = robot

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
            or digit not in 0..3
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setDigit." + char + "." + str(digit))

    def setBinary(self, value, digit):
        '''
        Shows the pattern of the binary value 0..255.
        @param value: the byte value
        @param digit: the display ID (0 is leftmost, 3 is rightmost)
        @return: True, if successful; False, if value not in 0..255 or digit not in 0..3
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setBinary." + str(value) + "." + str(digit))

    def setDecimalPoint(self, id):
        '''
        Shows one of the 3 decimal points.
        @param id: select the DP to show: 0: right bottom, 1: middle bottom, 2: middle top
        @return: True, if successful; False, if id not in 0..2
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setDecimalPoint." + str(id))

    def clearDigit(self, digit):
        '''
        Clears the given digit.
        @param digit: the display ID (0 is right most, 3 is left most)
        @return: True, if successful; False, if digit not in 0..3
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".clearDigit." + str(digit))

    def clear(self):
        '''
        Turns all digits off. Stops a running display thread.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".clear")

    def setText(self, text, dp = [0, 0, 0]):
        '''
        Displays the given text using an display thread. If the text to display exceeds 4 digits,
        only the 4 leading digits are shown. Because only one digit can be used at the same time,
        an internal display thread is created that drives the digits repeatedly in a fast sequence.
        Call clear() to stop the thread when it is no longer used. To display decimal points, use the
        dp paramater [right bottom, middle bottom, middle top] and set the decimal point values to 1
        @param text: the text to display (string or integer)
        @param dp: a list with three 1 or 0, if the decimal point is shown or not
        '''
        self._checkRobot()
        if not (type(text) == int or type(text) == list or type(text) == str):
            return
        if type(text) == int:
            text = str(text)
        text = text[0:4]

        self.robot.sendCommand(self.device + ".setText." + text + "." + \
           str(dp[0]) + ", " + str(dp[1]) + ", " + str(dp[2]))

    def setScrollableText(self, text, pos = 0):
        '''
        Displays a text that can be scrolled. A text position index is used that
        determines the character displayed at leftmost digit. Default pos = 0
        @param text: the text displayed
        @param pos: the start value of the text pointer (character index positioned a leftmost digit)
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setScrollableText." + text + "." + str(pos))

    def scrollToLeft(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the right
        '''
        self._checkRobot()
        return int(self.robot.sendCommand(self.device + ".scrollToLeft"))

    def scrollToRight(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the left
        '''
        self._checkRobot()
        return int(self.robot.sendCommand(self.device + ".scrollToRight"))

    def setToStart(self):
        '''
        Shows the scrollable text at the start position.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setToStart")

    def ticker(self, text, count = 1, speed = 2, blocking = False):
        '''
        Shows a ticker text that scroll to left until the last 4 characters are displayed.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 1). For count == 0, infinite duration,
        stopped by calling stopTicker()
        @param speed: the speed number of scrolling operations per sec (default: 2)
        @param blocking: if True, the method blocks until the ticker has finished; otherwise
         it returns immediately (default: False)
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".ticker." + text + "." + \
                str(count) + "." + str(speed))

    def stopTicker(self):
        '''
        Stops a running ticker.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".stopTicker")

    def getDisplayableChars(self):
        '''
        Returns a string with all displayable characters.
        @return: The character set that can be displayed
        '''
        self._checkRobot()
        return self.robot.sendCommand(self.device + ".getDisplayableChars")

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

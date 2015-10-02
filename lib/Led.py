# Led.java

'''
 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

from Tools import Tools
from RobotInstance import RobotInstance

class Led():
    '''
    Class that represents a LED pair.
    '''
    def __init__(self, id):
        '''
        Creates a Led instance with given ID.
        IDs of the double LEDs: 0: front, 1: left side , 2: rear, 3: right side.
        The following global constants are defined:
        LED_FRONT = 0, LED_LEFT = 1, LED_REAR = 2, RED_RIGHT = 3.
        @param id: the LED identifier
        '''
        self.id = id
        self.robot = RobotInstance.getRobot()
        Tools.debug("Led instance with ID " + str(id) + " created")

    def setColor(self, *args):
        '''
        Sets the RGB color value of the two LEDs with current ID.
        @param args list of [red, green, blue] RGB color components 0..255
            or three color integers 0..255
        '''
        self._checkRobot()
        if len(args) == 1 and type(args[0]) == list:
            red = int(args[0][0] / 255.0 * 4095)
            green = int(args[0][1] / 255.0 * 4095)
            blue = int(args[0][2] / 255.0 * 4095)
        elif len(args) == 3:
            red = int(args[0] / 255.0 * 4095)
            green = int(args[1] / 255.0 * 4095)
            blue = int(args[2] / 255.0 * 4095)
        else:
            raise ValueError("Illegal param in setColor()")
        id = (self.id + 3) % 4
        self.robot.pwm.setPWM(3 * id, 0, blue)
        self.robot.pwm.setPWM(3 * id + 1, 0, green)
        self.robot.pwm.setPWM(3 * id + 2, 0, red)

    @staticmethod
    def setColorAll(*args):
        '''
        Sets the RGB color of all 4 LED pairs.
        @param color list of [red, green, blue] RGB color components 0..255
         or three color integers 0..255
        '''
        leds = [Led(0), Led(1), Led(2), Led(3)]
        for led in leds:
            led.setColor(*args)

    @staticmethod
    def clearAll():
        '''
        Turns off all 4 LED pairs.
        '''
        Led.setColorAll(0, 0, 0)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")


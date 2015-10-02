# Gear.java

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
import SharedConstants
from RobotInstance import RobotInstance

class GearState():
    FORWARD = 0
    BACKWARD = 1
    STOPPED = 2
    LEFT = 3
    RIGHT = 4
    LEFTARC = 5
    RIGHTARC = 6
    UNDEFINED = 7

# ------------------------   Class Gear   --------------------------------------------------
class Gear(object):
    '''
    Class that represents the combination of two motors on an axis
    to perform a car-like movement.
    '''
    def __init__(self):
        '''
        Creates a gear instance.
        '''
        self.speed = SharedConstants.GEAR_DEFAULT_SPEED
        self.state = GearState.UNDEFINED
        Tools.debug("Gear instance created")

    def forward(self, duration = 0):
        '''
        Starts the forward rotation with preset speed.
        If duration = 0, the method returns immediately, while the rotation continues.
        Otherwise the method blocks until the duration is expired. Then the gear stops.
        @param duration: if greater than 0, the method blocks for the given duration (in ms)
        @type duration: int
        '''
        Tools.debug("Calling Gear.forward() with speed " + str(self.speed))
        self._checkRobot()
        if self.state != GearState.FORWARD:
            leftDuty = self.speedToDutyCycle(self.speed + SharedConstants.GEAR_FORWARD_SPEED_DIFF)
            rightDuty = self.speedToDutyCycle(self.speed)
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(leftDuty)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(rightDuty)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)
            self.state = GearState.FORWARD
        if duration > 0:
            Tools.delay(duration)
            self.stop()

    def backward(self, duration = 0):
        '''
        Starts the backward rotation with preset speed.
        If duration = 0, the method returns immediately, while the rotation continues.
        Otherwise the method blocks until the duration is expired. Then the gear stops.
        @param duration if greater than 0, the method blocks for the given duration (in ms)
        '''
        Tools.debug("Calling Gear.backward() with speed " + str(self.speed))
        self._checkRobot()
        if self.state != GearState.BACKWARD:
            leftDuty = self.speedToDutyCycle(self.speed + SharedConstants.GEAR_BACKWARD_SPEED_DIFF)
            rightDuty = self.speedToDutyCycle(self.speed)
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(leftDuty)
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(rightDuty)
            self.state = GearState.BACKWARD
        if duration > 0:
            Tools.delay(duration)
            self.stop()

    def left(self, duration = 0):
        '''
        Starts turning left with right motor rotating forward and
        left motor rotating backward at preset speed.
        If duration = 0, the method returns immediately, while the rotation continues.
        Otherwise the method blocks until the duration is expired. Then the gear stops.
        @param duration if greater than 0, the method blocks for the given duration (in ms)
        '''
        Tools.debug("Calling Gear.left()")
        self._checkRobot()
        if self.state != GearState.LEFT:
            duty = self.speedToDutyCycle(self.speed)
            duty = self.speedToDutyCycle(self.speed)
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(duty)
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(duty)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)
            self.state = GearState.LEFT
        if duration > 0:
            Tools.delay(duration)
            self.stop()

    def right(self, duration = 0):
        '''
        Starts turning right with left motor rotating forward and
        right motor rotating backward at preset speed.
        If duration = 0, the method returns immediately, while the rotation continues.
        Otherwise the method blocks until the duration is expired. Then the gear stops.
        @param duration if greater than 0, the method blocks for the given duration (in ms)
        '''
        Tools.debug("Calling Gear.right()")
        self._checkRobot()
        if self.state != GearState.RIGHT:
            duty = self.speedToDutyCycle(self.speed)
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(duty)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(duty)
            self.state = GearState.RIGHT
        if duration > 0:
            Tools.delay(duration)
            self.stop()

    def leftArc(self, radius, duration = 0):
        '''
        Starts turning to the left on an arc with given radius (in m) with preset speed.
        If duration = 0, the method returns immediately, while the rotation continues.
        Otherwise the method blocks until the duration is expired. Then the gear stops.
        If the radius is negative, turns left backwards.
        @param duration:
        @return:
        '''
        Tools.debug("Calling Gear.leftArc() with radius: " + str(radius))
        self._checkRobot()
        speed1 = \
            self.speed * (abs(radius) - SharedConstants.GEAR_AXE_LENGTH) / (abs(radius) + SharedConstants.GEAR_AXE_LENGTH)
        Tools.debug("Calling leftArc(). Left speed: " + str(speed1) + ". Right speed: " + str(self.speed))
        if self.state != GearState.LEFTARC:
            leftDuty = self.speedToDutyCycle(speed1)
            rightDuty = self.speedToDutyCycle(self.speed)
            if radius >= 0:
                SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(leftDuty)
                SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
                SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(rightDuty)
                SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)
            else:
                SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
                SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(rightDuty)
                SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
                SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(leftDuty)
            self.state = GearState.LEFTARC
        if duration > 0:
            Tools.delay(duration)
            self.stop()

    def leftArcMilli(self, radius, duration = 0):
        '''
        Same as leftArc(radius, duration), but radius in mm
        @param radius in mm
        '''
        self.leftArc(radius / 1000.0, duration)

    def rightArc(self, radius, duration = 0):
        '''
        Starts turning to the right on an arc with given radius (in m) with preset speed.
        If duration = 0, the method returns immediately, while the rotation continues.
        Otherwise the method blocks until the duration is expired. Then the gear stops.
        If the radius is negative, turns right backwards.
        @param duration:
        '''
        Tools.debug("Calling Gear.rigthArc() with radius: " + str(radius))
        self._checkRobot()
        speed1 = \
            self.speed * (abs(radius) - SharedConstants.GEAR_AXE_LENGTH) / (abs(radius) + SharedConstants.GEAR_AXE_LENGTH)
        Tools.debug("Calling rightArc(). Left speed: " + str(self.speed) + ". Right speed: " + str(speed1))
        if self.state != GearState.RIGHTARC:
            leftDuty = self.speedToDutyCycle(self.speed)
            rightDuty = self.speedToDutyCycle(speed1)
            if radius >= 0:
                SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(leftDuty)
                SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
                SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(rightDuty)
                SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)
            else:
                SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
                SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(rightDuty)
                SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
                SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(leftDuty)
            self.state = GearState.RIGHTARC
        if duration > 0:
            Tools.delay(duration)
            self.stop()

    def rightArcMilli(self, radius, duration = 0):
        '''
        Sama as rightArc(radius, duration), but radius in mm
        @param radius in mm
        '''
        self.rightArc(radius / 1000.0, duration)

    def stop(self):
        '''
        Stops the gear.
        (If gear is already stopped, returns immediately.)
        '''
        Tools.debug("Calling Gear.stop()")
        self._checkRobot()
        if self.state != GearState.STOPPED:
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)
            self.state = GearState.STOPPED

    def setSpeed(self, speed):
        '''
        Sets the speed to the given value (arbitrary units).
        The speed will be changed to the new value at the next movement call only.
        The speed is limited to 0..100.
        @param speed: the new speed 0..100
        '''
        Tools.debug("Calling Gear.setSpeed with speed: " + str(speed))
        if self.speed == speed:
            return
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0
        self.speed = speed
        self.state = GearState.UNDEFINED

    def speedToDutyCycle(self, speed):
        '''
        Linear relationship for mapping speed 0..100 to duty cycle
        '''
        if speed < 0:
            return 0
        elif speed > 100:
            return 100
        return speed

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")



# Motor.java

'''
Class that represents a motor.

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

# ------------------------   Class MotorState  ----------------------------------------------
class MotorState():
    FORWARD = 0
    BACKWARD = 1
    STOPPED = 2
    UNDEFINED = 3

# ------------------------   Class Motor  ---------------------------------------------------
class Motor():
    '''
    Class that represents a motor.
    '''
    def __init__(self, id):
        '''
        Creates a motor instance with given id.
        @param id: 0 for left motor, 1 for right motor
        '''
        self.id = id
        self.speed = SharedConstants.MOTOR_DEFAULT_SPEED
        self.state = MotorState.UNDEFINED
        self.pwm = [0] * 2
        if self.id == SharedConstants.MOTOR_LEFT:
            self.pwm[0] = SharedConstants.LEFT_MOTOR_PWM[0]
            self.pwm[1] = SharedConstants.LEFT_MOTOR_PWM[1]
        else:
            self.pwm[0] = SharedConstants.RIGHT_MOTOR_PWM[0]
            self.pwm[1] = SharedConstants.RIGHT_MOTOR_PWM[1]

    def forward(self):
        '''
        Starts the forward rotation with preset speed.
        The method returns immediately, while the rotation continues.
          '''
        Tools.debug("Calling Motor.forward()")
        if self.state == MotorState.FORWARD:
            return
        self._checkRobot()
        duty = self.speedToDutyCycle(self.speed)
        if self.id == SharedConstants.MOTOR_LEFT:
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(duty)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
        else:
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(duty)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)

        self.state = MotorState.FORWARD
        Tools.debug("Done Motor.forward()")

    def backward(self):
        '''
        Starts the backward rotation with preset speed.
        The method returns immediately, while the rotation continues.
        '''
        Tools.debug("Calling Motor.backward(). MotorID: " + str(self.id))
        if self.state == MotorState.BACKWARD:
            return
        self._checkRobot()
        duty = self.speedToDutyCycle(self.speed)
        if self.id == SharedConstants.MOTOR_LEFT:
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(duty)
        else:
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(duty)
        self.state = MotorState.BACKWARD
        Tools.debug("Done Motor.backward()")

    def stop(self):
        '''
        Stops the motor.
        (If motor is already stopped, returns immediately.)
        '''
        Tools.debug("Calling Motor.stop(). MotorID: " + str(self.id))
        if self.state == MotorState.STOPPED:
            return
        self._checkRobot()
        if self.id == SharedConstants.MOTOR_LEFT:
            SharedConstants.LEFT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.LEFT_MOTOR_PWM[1].ChangeDutyCycle(0)
        else:
            SharedConstants.RIGHT_MOTOR_PWM[0].ChangeDutyCycle(0)
            SharedConstants.RIGHT_MOTOR_PWM[1].ChangeDutyCycle(0)
        self.state = MotorState.STOPPED
        Tools.debug("Done Motor.stop()")

    def setSpeed(self, speed):
        '''
        Sets the speed to the given value (arbitrary units).
        The speed will be changed to the new value at the next movement call only.
        The speed is limited to 0..100.
        @param speed: the new speed 0..100
        '''
        if speed > 100:
            speed = 100
        if speed < 0:
            speed = 0
        if self.speed == speed:
            return
        self.speed = speed
        self.state = MotorState.UNDEFINED

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



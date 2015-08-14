# RobotInstance.py

'''
Holder of global Robot instance
'''
class RobotInstance():
    _robot = None

    @staticmethod
    def setRobot(robot):
        RobotInstance._robot = robot

    @staticmethod
    def getRobot():
        return RobotInstance._robot

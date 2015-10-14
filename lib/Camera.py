# Camera.java

'''
Class that represents a camera attached to servo motor platform.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code777
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

from Tools import Tools
from RobotInstance import RobotInstance
import picamera
import StringIO

class Camera():
    '''
     Class that represents a camera attached to servo motor platform.
     Horizontal servo at servo port 1 (S13 header)
     Vertical servo at servo port 2 (S14 header)
    '''
    def __init__(self):
        '''
        Creates a camera instance.
        '''
        Tools.debug("Camera instance created")

    def captureJPEG(self, width, height):
        '''
        Takes a camera picture with given picture size and returns the image
        in JPEG format. The picture resolution is width x height (max: 5 MPix)
        @param width: the width of the picture in pixels (max: 2592)
        @param height: the height of the picture in pixels (max: 1944)
        return: the image in JPEG format (as string); None, if the capture fails
        '''
        self._checkRobot()
        camera = picamera.PiCamera()
        imageData = StringIO.StringIO()
        w = int(width)
        h = int(height)

        try:
            Tools.debug("Camera capture with (width, height) = (%d, %d)" % (w, h))
            camera.capture(imageData, format = "jpeg", resize = (w, h))
            imageData.seek(0)
            data = imageData.getvalue()
            Tools.debug("Captured jpeg size: " + str(len(data)))
            return data
        finally:
            camera.close()
        return None  # error

    def saveData(self, data, filename):
        '''
        Writes the given string data into a binary file.
        @param data: the data to store (as string type)
        @param filename: a valid filename in the local file space
        '''
        file = open(filename, "wb")
        file.write(data)
        file.close()

    def captureAndSave(self, width, height, filename):
        '''
        Takes a camera picture with given picture size and stores is
        in JPEG format.
        The picture resolution is width x height (max: 5 MPix)
        @param width: the width of the picture in pixels (max: 2592)
        @param height: the height of the picture in pixels (max: 1944)
        @param filename: a valid filename in the local file space, e.g. /home/pi/shot1.jpg
        '''
        data = self.captureJPEG(width, height)
        if data != None:
            self.saveData(data, filename)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")


# Tools.py

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

import time
import SharedConstants

class Tools():
    '''
    Helper class with some useful static methods.
    '''
    @staticmethod
    def debug(text):
        if SharedConstants.DEBUG:
            print text

    @staticmethod
    def delay(interval):
        """
        Suspends execution for a given time inverval.
        @param interval: the time interval in milliseconds (ms)
        @return: none
        """
        time.sleep(interval / 1000.0)




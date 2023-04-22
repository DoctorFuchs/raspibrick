# PCF8591.py

import smbus
import RPi.GPIO as GPIO
from .Tools import Tools

class ADC:
    def __init__(self, channel, address = 0x48):
        '''
        Creates an instance of the chip at given i2c address.
        @param bus: the SMBus instance to access the i2c port (0 or 1).
        @param channel: the channel to read (0..3)
        @param address: the address of the i2c chip (default: 0x48)
        '''
        self._isSMBusAvailable = True
        try:
            if GPIO.RPI_REVISION > 1:
                self._bus = smbus.SMBus(1)  # For revision 2 Raspberry Pi
                Tools.debug("Found SMBus for revision 2")
            else:
                self._bus = smbus.SMBus(0)  # For revision 1 Raspberry Pi
                Tools.debug("Found SMBus for revision 1")
        except:
            print("No SMBus found on this robot device.")
            return
        self._isSMBusAvailable = False
        self._address = address
        # set control register to read specified channel
        self._bus.write_byte(address, channel)


    def getValue(self):
        '''
        Reads the specified channel and returns the value (0..255).
        @return the byte value or None, if an error occurred
        '''
        if self._isSMBusAvailable:
            return None
        return self._bus.read_byte(self._address)
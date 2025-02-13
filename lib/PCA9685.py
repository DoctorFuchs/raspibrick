# PCA9685.py
# ============================================================================
# Most code from Adafruit PCA9685 16-Channel PWM Servo Driver
# with thanks to the author
# ============================================================================

import time
import math
from .Tools import Tools

class PWM:
    _mode_adr              = 0x00
    _base_adr_low          = 0x08
    _base_adr_high         = 0x09
    _prescale_adr          = 0xFE

    def __init__(self, bus, address = 0x40):
        '''
        Creates an instance of the PWM chip at given i2c address.
        @param bus: the SMBus instance to access the i2c port (0 or 1).
        @param address: the address of the i2c chip (default: 0x40)
        '''
        self.bus = bus
        self.address = address
        self._isAvailable = True
        self._writeByte(self._mode_adr, 0x00)

    def setFreq(self, freq):
        '''
        Sets the PWM frequency. The value is stored in the device.
        @param freq: the frequency in Hz (approx. in range 16 - 1500 Hz)
        '''
        if not self._isAvailable:
            return
        prescaleValue = 25000000.0    # 25MHz
        prescaleValue /= 4096.0       # 12-bit
        prescaleValue /= float(freq)
        prescaleValue -= 1.0
        prescale = math.floor(prescaleValue + 0.5)
        oldmode = self._readByte(self._mode_adr)
        if oldmode == None:
            return
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        self._writeByte(self._mode_adr, newmode)  # goto sleep
        self._writeByte(self._prescale_adr, int(math.floor(prescale)))
        self._writeByte(self._mode_adr, oldmode)
        time.sleep(0.005)
        self._writeByte(self._mode_adr, oldmode | 0x80)

    def setDuty(self, channel, duty):
        '''
        Sets a single PWM channel. The value is stored in the device.
        @param channel: one of the channels 0..15
        @param duty: the duty cycle 0..4095 (included)
        '''
        if not self._isAvailable:
            return
        duty = int(duty)
        duty = max(0, duty)
        duty = min(4095, duty)
        self._writeByte(self._base_adr_low + 4 * channel, duty & 0xFF)
        self._writeByte(self._base_adr_high + 4 * channel, duty >> 8)

    def _writeByte(self, reg, value):
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except:
            Tools.debug("Error while writing to I2C device at address: " + str(self.address))
            self._isAvailable = False

    def _readByte(self, reg):
        try:
            result = self.bus.read_byte_data(self.address, reg)
            return result
        except:
            Tools.debug("Error while reading from I2C device at address: " + str(self.address))
            return None

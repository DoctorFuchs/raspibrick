# Infrared4.py
# TCRT5000 with ADC MCP3021

import smbus
import time

bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x4D  # default address
t = 0
while True:
    # Reads word (2 bytes) as int
    rd = bus.read_word_data(i2c_address, 0)
    # Exchanges high and low bytes
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
    data = data >> 2
    print(t, "v:", data)
    t += 0.1
    time.sleep(0.1)

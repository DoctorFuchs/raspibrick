# LightSIM800.py
# LM35 temperature sensor sending data to Web server

import serial
import time, sys
from SIM800Modem import *
import smbus
from OLED1306 import OLED1306

APN = "gprs.swisscom.ch"
HOST = "www.aplu.dx.am"
PORT = 80

SERIAL_PORT = "/dev/ttyAMA0"  # Raspberry Pi 2
#SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi 3

def readData(port = 0):
    if port == 0:
        adc_address = 0x48
    elif port == 1:    
        adc_address = 0x4D
    rd = bus.read_word_data(adc_address, 0)
    data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    data = data >> 2
    return data

oled = OLED1306()
bus = smbus.SMBus(1) 
oled.setText("Resetting modem...")
print("Resetting modem...")
resetModem()
ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
if not isReady(ser):
    print("Modem not ready.")
    oled.setText("Modem not ready.")
    sys.exit(0)

print("Connecting to GSM net...")
oled.setText("Connecting to GSM net...")
connectGSM(ser, APN)
while True:
    startTime = time.time()
    t = datetime.datetime.now()
    t = str(t)
    k = t.find(".")
    t = t[:k]
    x = t.replace(" ", "%20") # don't use space in url
    v = readData(1)
    y = v / 3.1
    y = "%4.1f" %y
    print("t = ", t, ":-- T =", y, "centigrades") 
    oled.setText("At = " + str(t), 0)
    oled.setText("T = " + y + " centigrades", 1)
    print("Sending HTTP request...")
    reply = connectTCP(ser, HOST, PORT)
    if "CONNECT OK" not in reply:
        print("Connection failed")
        sys.exit(0)
    sendHTTPRequest(ser, HOST, "/insert.php?x=" + x + "&y=" + y) 
    print("Closing. Waiting for next transfer")
    closeTCP(ser)
    isRunning = True
    while time.time() - startTime < 60:
       time.sleep(0.1)

# WebServer2.py

import serial
import time, sys
from math import exp, cos
from SIM800Modem import *

def f(x):
    return 0.5 + 0.5 * exp(-0.01 * x) * cos(0.1 * x) 

APN = "gprs.swisscom.ch"
HOST = "www.aplu.dx.am"
PORT = 80

SERIAL_PORT = "/dev/ttyS0"    # Raspberry Pi 3
table = "data01"

print "Resetting modem..."
resetModem()
ser = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 5)
if not isReady(ser):
    print "Modem not ready."
    sys.exit(0)

print "Connecting to GSM net..."
connectGSM(ser, APN)
x = 0
dx = 5
while x <= 100:
    y = f(x)
    print x, y
    print "Sending HTTP request..."
    reply = connectTCP(ser, HOST, PORT)
    if "CONNECT OK" not in reply:
        print "Connection failed"
        sys.exit(0)
    print "Sending HTTPRequest..."    
    sendHTTPRequest(ser, HOST, "/insert.php?table=" + table + "&x=" + str(x) + "&y=" + str(y)) 
    print "Closing. Waiting for next transfer"
    closeTCP(ser)
    x += dx
    time.sleep(dx)


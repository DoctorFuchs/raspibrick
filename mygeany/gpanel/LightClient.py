# LightClient.py

from gpanel import *
from tcpcom import TCPClient

def onStateChanged(state, msg):
    global value
    if state == "MESSAGE":
        value = msg

makeGPanel(-1, 11, -0.1, 1.1)
title("LightSensor")

HOST = "192.168.0.6"
PORT = 5000 # IP port
client = TCPClient(HOST, PORT, stateChanged = onStateChanged)
rc = client.connect()
value = 500
if rc:
    while True:
        clear()
        t = 0
        setPenColor("gray")
        drawGrid(0, 10, 0, 1.0)
        setPenSize(2)
        setPenColor("blue")
        while t <= 10:
            v = int(value) / 1023.0 
            if t == 0:
                pos(0, v)
            else:   
                draw(t, v)
            t += 0.1
            delay(100)


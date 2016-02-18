# EchoServer.py

from raspibrick import *

def onStateChanged(state, msg):
    if state == TCPServer.LISTENING:
      display.showText("LIS");
    elif state == TCPServer.CONNECTED:
      display.showText("conn")
    elif state == TCPServer.MESSAGE:
      display.showText(msg)
      server.sendMessage(msg)

robot = Robot()
display = Display()
port = 5000    
server = TCPServer(port, stateChanged = onStateChanged)
while not isEscapeHit():
    pass        
server.terminate()
display.showText("End")
Tools.delay(1000)
robot.exit()


# LightSensor2.py

from raspibrick import *

robot = Robot()
sensorList = []
for id in range(4):
    ls = LightSensor(id)
    sensorList.append(ls)
while not robot.isButtonHit():
    for id in range(4):
        print id, ":", sensorList[id].getValue(), ";",
    print ""
    Tools.delay(100)
robot.exit()
print "All done"
from raspibrick import *

robot = Robot()
gear = Gear()
uss = UltrasonicSensor()
gear.forward()
while not isEscapeHit():
    v = uss.getValue()
    if v < 15:
        gear.backward(3000)
        gear.forward()
robot.exit()
print "All done"

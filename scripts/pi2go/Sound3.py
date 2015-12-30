# Sound3.py

from raspibrick import *

def onButtonEvent(event):
    global isTurnedOn, volume, isIncreasing, trackNb
    if event == SharedConstants.BUTTON_CLICKED:
        if isIncreasing:
            volume += 10
        else:
            volume -= 10
        if volume == 100:
            isIncreasing = False
        if volume == 0:
            isIncreasing = True
        print "setting volume to", volume
        display.showText("L" + str(volume))
        robot.setSoundVolume(volume)
    elif event == SharedConstants.BUTTON_DOUBLECLICKED:
        robot.stopSound()
    elif event == SharedConstants.BUTTON_LONGPRESSED:
        isTurnedOn = False
        print "Terminating..."
        display.showText("donE")


robot = Robot()
robot.addButtonListener(onButtonEvent, True)
display = Display()

volume = 50
isIncreasing = True
trackNb = 1
isError = False
rc = robot.initSound("/home/pi/salza1.wav", volume)
if rc:
    robot.playSound()
    display.showText("x" + str(trackNb))
    print "init ok"
    isTurnedOn = True
    while isTurnedOn and not isError:
        if not robot.isSoundPlaying():
            trackNb += 1
            if trackNb == 11:
                trackNb = 1
            display.showText("x" + str(trackNb))
            robot.closeSound()
            rc = robot.initSound("/home/pi/salza" + str(trackNb) + ".wav", volume)
            robot.playSound()
            if not rc:
               isError = True
        Tools.delay(1000)
else:
    display.showText("FAIL")
    print "init failed"
    Tools.delay(2000)
if isError:
    display.showBlinker("Err", [0], 3, 1, True)
display.showText("donE")
Tools.delay(3000)
robot.exit()  # stops sound and closes sound channel
print "All done"


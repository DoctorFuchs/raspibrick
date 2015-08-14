import RPi.GPIO as GPIO
import time
import sys
from xAdafruit_PWM_Servo_Driver import PWM

# LED PWM frequency
LED_PWM_FREQ = 50


def setColor(id, red, green, blue):
    red = int(red / 255.0 * 4095)
    green = int(green / 255.0 * 4095)
    blue = int(blue / 255.0 * 4095)
    myid = (id + 3) % 4
    ledPWM.setPWM(3 * id, 0, blue)
    ledPWM.setPWM(3 * id + 1, 0, green)
    ledPWM.setPWM(3 * id + 2, 0, red)

print "Trying to detect PCA9685 PCM chip on I2C bus using bus number 0..."
try:
    ledPWM = PWM(0x40, busnumber = 0, debug = False)
    ledPWM.setPWMFreq(LED_PWM_FREQ)
    print "PCA9685 PCM chip on I2C bus #0 detected"
except Exception as e:
    print "Failed, trying with bus number 1..."
    try:
        ledPWM = PWM(0x40, busnumber = 1, debug = False)
        ledPWM.setPWMFreq(LED_PWM_FREQ)
        print "PCA9685 PCM chip on I2C bus #1 detected"
    except:
        print "Failed to detect PCA9685 PCM chip on I2C bus"
        sys.exit(1)

for id in range(4):
    print "Led", id
    setColor(id, 128, 0, 0)
    time.sleep(1)
    setColor(id, 0, 128, 0)
    time.sleep(1)
    setColor(id, 0, 0, 128)
    time.sleep(1)
    setColor(id, 0, 0, 0)
    time.sleep(1)
print "All done"
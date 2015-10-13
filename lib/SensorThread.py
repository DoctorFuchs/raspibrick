# SensorThread.py

from threading import Thread
from Tools import *
import SharedConstants

class SensorThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sensors = []
        self.isSensorThreadRunning = True

    def run(self):
        print "Sensor thread started"
        while self.isSensorThreadRunning:
            for sensor in self.sensors:
                if sensor.getSensorType() == "LightSensor":
                    v = sensor.getValue()
                    if v > sensor.getTriggerLevel() and sensor.getSensorState() == "DARK":
                        sensor.setSensorState("BRIGHT")
                        sensor.onBright(v)
                    if v <= sensor.getTriggerLevel() and sensor.getSensorState() == "BRIGHT":
                        sensor.setSensorState("DARK")
                        sensor.onDark(v)
                if sensor.getSensorType() == "InfraredSensor":
                    v = sensor.getValue()
                    if v == 1 and sensor.getSensorState() == "DARK":
                        sensor.setSensorState("BRIGHT")
                        sensor.onBright()
                    if v == 0 and sensor.getSensorState() == "BRIGHT":
                        sensor.setSensorState("DARK")
                        sensor.onDark()
                if sensor.getSensorType() == "UltrasonicSensor":
                    v = sensor.getValue()
                    if v > sensor.getTriggerLevel() and sensor.getSensorState() == "NEAR":
                        sensor.setSensorState("FAR")
                        sensor.onFar(v)
                    if v <= sensor.getTriggerLevel() and sensor.getSensorState() == "FAR":
                        sensor.setSensorState("NEAR")
                        sensor.onNear(v)
            Tools.delay(SharedConstants.POLL_DELAY)
        print "Sensor thread terminated"

    def stop(self):
        self.isSensorThreadRunning = False

    def add(self, sensor):
        self.sensors.append(sensor)

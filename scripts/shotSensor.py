import asyncio
from apds9960.const import *
from apds9960 import APDS9960
import smbus

class ShotSensor:
    def __init__(self):
        self.i2c_bus = smbus.SMBus(1)
        self.apds = APDS9960(self.i2c_bus)
        self.apds.enableGestureSensor()
        self.shot_detected = False
        
    async def monitor_shots(self):
        while True:
            if self.apds.isGestureAvailable():
                print("Gesture detected")
                gesture = self.apds.readGesture()
                #if gesture == APDS9960_DIR_DOWN:
                self.shot_detected = True
            await asyncio.sleep(0.5)
            
    def reset_shot(self):
        self.shot_detected = False
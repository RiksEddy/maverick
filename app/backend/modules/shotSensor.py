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
            try:
                if self.apds.isGestureAvailable():
                    gesture = self.apds.readGesture()
                    self.shot_detected = True
            except Exception as e:
                print(f"Error in shot monitoring: {e}")  # Debug print
            await asyncio.sleep(0.5)  # Reduced sleep time for more responsive detection
            
    def reset_shot(self):
        self.shot_detected = False
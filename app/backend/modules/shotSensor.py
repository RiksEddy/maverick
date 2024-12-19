import asyncio
from apds9960.const import *
from apds9960 import APDS9960
import smbus

class ShotSensor:
    def __init__(self):
        print("Initializing Shot Sensor...")  # Debug print
        self.i2c_bus = smbus.SMBus(1)
        self.apds = APDS9960(self.i2c_bus)
        self.apds.enableGestureSensor()
        self.shot_detected = False
        print("Shot Sensor initialized")  # Debug print
        
    async def monitor_shots(self):
        print("Starting shot monitoring...")  # Debug print
        while True:
            try:
                if self.apds.isGestureAvailable():
                    print("Gesture detected!")  # Debug print
                    gesture = self.apds.readGesture()
                    print(f"Gesture value: {gesture}")  # Debug print
                    self.shot_detected = True
                    print("Shot detected flag set to True")  # Debug print
            except Exception as e:
                print(f"Error in shot monitoring: {e}")  # Debug print
            await asyncio.sleep(0.1)  # Reduced sleep time for more responsive detection
            
    def reset_shot(self):
        print("Resetting shot detection")  # Debug print
        self.shot_detected = False
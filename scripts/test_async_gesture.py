import asyncio
from apds9960.const import *
from apds9960 import APDS9960
import smbus

class GestureSensor:
    def __init__(self):
        self.i2c_bus = smbus.SMBus(1)
        self.apds = APDS9960(self.i2c_bus)
        self.apds.enableGestureSensor()
        self.last_gesture = None
        self.gesture_count = 0
        
    async def monitor_gestures(self):
        while True:
            if self.apds.isGestureAvailable():
                gesture = self.apds.readGesture()
                self.gesture_count += 1
                await self.handle_gesture(gesture)
            await asyncio.sleep(0.1)
            
    async def handle_gesture(self, gesture):
        if gesture == APDS9960_DIR_UP:
            self.last_gesture = "UP"
        elif gesture == APDS9960_DIR_DOWN:
            self.last_gesture = "DOWN"
        else:
            self.last_gesture = "UNKNOWN"
        print(self.last_gesture)
            
    async def print_statistics(self):
        while True:
            print(f"Total gestures detected: {self.gesture_count}")
            print(f"Last gesture: {self.last_gesture}")
            await asyncio.sleep(5)  # Print stats every 5 seconds

async def main():
    sensor = GestureSensor()
    
    # Create multiple tasks
    gesture_task = asyncio.create_task(sensor.monitor_gestures())
    stats_task = asyncio.create_task(sensor.print_statistics())
    
    try:
        print("Gesture sensor is running. Press Ctrl+C to exit.")
        # Wait for all tasks
        await asyncio.gather(gesture_task, stats_task)
        
    except asyncio.CancelledError:
        print("Tasks cancelled")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
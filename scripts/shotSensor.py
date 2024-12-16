import asyncio
from apds9960.const import *
from apds9960 import APDS9960
import smbus

class ShotSensor:
    def __init__(self):
        self.i2c_bus = smbus.SMBus(1)
        self.apds = APDS9960(self.i2c_bus)
        self.apds.enableGestureSensor()
        self.last_shot_direction = None
        self.shot_count = 0
        
    async def monitor_shots(self):
        while True:
            if self.apds.isGestureAvailable():
                gesture = self.apds.readGesture()
                self.shot_count += 1
                await self.handle_motion(gesture)
            await asyncio.sleep(0.1)
            
    async def handle_motion(self, gesture):
        if gesture == APDS9960_DIR_DOWN:
            self.last_shot_direction = "DOWN"
        #elif gesture == APDS9960_DIR_UP:
        #    self.last_shot_direction = "UP"
        print(self.last_shot_direction)
            
    async def print_statistics(self):
        while True:
            print(f"Total shots detected: {self.shot_count}")
            print(f"Last shot direction: {self.last_shot_direction}")
            await asyncio.sleep(5)  # Print stats every 5 seconds

async def main():
    sensor = ShotSensor()
    
    # Create multiple tasks
    monitor_task = asyncio.create_task(sensor.monitor_shots())
    stats_task = asyncio.create_task(sensor.print_statistics())
    
    try:
        print("Gesture sensor is running. Press Ctrl+C to exit.")
        # Wait for all tasks
        await asyncio.gather(monitor_task, stats_task)
        
    except asyncio.CancelledError:
        print("Tasks cancelled")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
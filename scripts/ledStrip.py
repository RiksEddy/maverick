import asyncio
from apds9960.const import *
from apds9960 import APDS9960
import smbus
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 30        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 10   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class LEDStrip:
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
                               LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        
    def colorWipe(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            
    def turn_off(self):
        """Turn off all LEDs."""
        self.colorWipe(Color(0, 0, 0))
        
    def turn_green(self):
        """Turn all LEDs green."""
        self.colorWipe(Color(0, 255, 0))

class ShotSensor:
    def __init__(self, led_strip):
        # Initialize shot sensor
        self.i2c_bus = smbus.SMBus(1)
        self.apds = APDS9960(self.i2c_bus)
        self.apds.enableGestureSensor()
        self.last_shot_direction = None
        self.shot_count = 0
        self.led_strip = led_strip
        
    async def monitor_shots(self):
        while True:
            if self.apds.isGestureAvailable():
                gesture = self.apds.readGesture()
                self.shot_count += 1
                await self.handle_motion(gesture)
                # Light up green when shot is detected
                self.led_strip.turn_green()
                # Wait a bit then turn off
                await asyncio.sleep(0.5)
                self.led_strip.turn_off()
            await asyncio.sleep(0.1)
            
    async def handle_motion(self, gesture):
        if gesture == APDS9960_DIR_DOWN:
            self.last_shot_direction = "DOWN"
        print(self.last_shot_direction)
            
    async def print_statistics(self):
        while True:
            print(f"Total shots detected: {self.shot_count}")
            print(f"Last shot direction: {self.last_shot_direction}")
            await asyncio.sleep(5)  # Print stats every 5 seconds

async def main():
    led_strip = LEDStrip()
    sensor = ShotSensor(led_strip)
    
    # Create multiple tasks
    monitor_task = asyncio.create_task(sensor.monitor_shots())
    stats_task = asyncio.create_task(sensor.print_statistics())
    
    try:
        print("Shot sensor is running. Press Ctrl+C to exit.")
        # Wait for all tasks
        await asyncio.gather(monitor_task, stats_task)
        
    except asyncio.CancelledError:
        print("Tasks cancelled")
        led_strip.turn_off()  # Turn off LEDs
    except Exception as e:
        print(f"Error occurred: {e}")
        led_strip.turn_off()  # Turn off LEDs

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
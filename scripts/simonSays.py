import asyncio
import random
import time
from apds9960.const import *
from apds9960 import APDS9960
import smbus
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 30        
LED_PIN = 18          
LED_FREQ_HZ = 800000  
LED_DMA = 10          
LED_BRIGHTNESS = 10   
LED_INVERT = False    
LED_CHANNEL = 0       

class LEDStrip:
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, 
                               LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()
        self.current_color = None
        
    def colorWipe(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
            
    def turn_off(self):
        """Turn off all LEDs."""
        self.current_color = None
        self.colorWipe(Color(0, 0, 0))
        
    def turn_red(self):
        """Turn all LEDs red."""
        self.current_color = "red"
        self.colorWipe(Color(255, 0, 0))
        
    def turn_green(self):
        """Turn all LEDs green."""
        self.current_color = "green"
        self.colorWipe(Color(0, 255, 0))
        
    def turn_blue(self):
        """Turn all LEDs blue."""
        self.current_color = "blue"
        self.colorWipe(Color(0, 0, 255))

class ShotSensor:
    def __init__(self, led_strip):
        self.i2c_bus = smbus.SMBus(1)
        self.apds = APDS9960(self.i2c_bus)
        self.apds.enableGestureSensor()
        self.shot_detected = False
        self.led_strip = led_strip
        
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

class SimonSaysGame:
    def __init__(self, led_strip, shot_sensor):
        self.led_strip = led_strip
        self.shot_sensor = shot_sensor
        self.score = 0
        self.colors = ["red", "green", "blue"]
        self.target_color = None
        self.game_active = True
        self.start_time = None
        self.game_duration = 60  # 60 seconds = 1 minute
        
    def choose_target_color(self):
        self.target_color = random.choice(self.colors)
        print(f"\nTarget color is: {self.target_color.upper()}")
        print("Shoot when you see this color!")
        
    async def cycle_colors(self):
        self.start_time = time.time()
        
        while self.game_active and time.time() - self.start_time < self.game_duration:
            # Cycle through colors
            for color_func in [self.led_strip.turn_red, 
                             self.led_strip.turn_green, 
                             self.led_strip.turn_blue]:
                if not self.game_active or time.time() - self.start_time >= self.game_duration:
                    break
                    
                color_func()
                await asyncio.sleep(5)  # Show each color for 5 seconds
                
                if self.shot_sensor.shot_detected:
                    print(f"Shot detected during {self.led_strip.current_color}")
                    if self.led_strip.current_color == self.target_color:
                        print("Great shot! +1 point")
                        self.score += 1
                    else:
                        print(f"Wrong color! -1 point. You shot during {self.led_strip.current_color}")
                        self.score -= 1
                    self.shot_sensor.reset_shot()
        
        self.game_active = False
        self.led_strip.turn_off()
        print("\nGame Over!")
        print(f"Final score: {game.score}")
                    
    async def print_score_and_time(self):
        while self.game_active:
            time_remaining = int(self.game_duration - (time.time() - self.start_time))
            if time_remaining <= 0:
                break
            print(f"\nTime remaining: {time_remaining} seconds")
            print(f"Current score: {self.score}")
            await asyncio.sleep(3)

async def main():
    led_strip = LEDStrip()
    shot_sensor = ShotSensor(led_strip)
    game = SimonSaysGame(led_strip, shot_sensor)
    
    print("\nWelcome to Simon Says!")
    print("Game will run for 1 minute")
    await asyncio.sleep(2)
    
    # Choose initial target color
    game.choose_target_color()
    
    # Create tasks
    monitor_task = asyncio.create_task(shot_sensor.monitor_shots())
    color_cycle_task = asyncio.create_task(game.cycle_colors())
    score_task = asyncio.create_task(game.print_score_and_time())
    
    try:
        print("Game starting in:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            await asyncio.sleep(1)
        print("GO!")
        
        # Wait for all tasks
        await asyncio.gather(monitor_task, color_cycle_task, score_task)
        
    except asyncio.CancelledError:
        print("Game cancelled!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGame stopped by user")
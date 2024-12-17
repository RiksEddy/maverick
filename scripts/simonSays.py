import asyncio
import random
import time
from ledStrip import LEDStrip
from shotSensor import ShotSensor

class SimonSaysGame:
    def __init__(self, led_strip, shot_sensor):
        self.led_strip = led_strip
        self.shot_sensor = shot_sensor
        self.score = 0
        self.colors = ["red", "green", "blue"]
        self.sequence = []
        self.current_sequence_index = 0
        self.game_active = True
        self.start_time = None
        self.game_duration = 60  # 60 seconds = 1 minute
        
    def generate_sequence(self, length=3):
        """Generate a random sequence of colors"""
        self.sequence = [random.choice(self.colors) for _ in range(length)]
        self.current_sequence_index = 0
        print("\nRemember this sequence:")
        for i, color in enumerate(self.sequence, 1):
            print(f"{i}: {color.upper()}")
        print("\nShoot the colors in this order!")
        
    async def show_sequence(self):
        """Display the sequence to memorize"""
        print("\nWatching sequence...")
        for color in self.sequence:
            if color == "red":
                self.led_strip.turn_red()
            elif color == "green":
                self.led_strip.turn_green()
            elif color == "blue":
                self.led_strip.turn_blue()
            await asyncio.sleep(2)
            self.led_strip.turn_off()
            await asyncio.sleep(0.5)
        
    async def show_random_colors(self):
        """Show random colors and check for correct shots"""
        while self.current_sequence_index < len(self.sequence):
            if not self.game_active:
                break
                
            # Randomly choose and show a color
            random_color = random.choice(self.colors)
            if random_color == "red":
                self.led_strip.turn_red()
            elif random_color == "green":
                self.led_strip.turn_green()
            elif random_color == "blue":
                self.led_strip.turn_blue()
                
            await asyncio.sleep(2)  # Show color for 2 seconds
            
            if self.shot_sensor.shot_detected:
                print(f"Shot detected during {self.led_strip.current_color}")
                if self.led_strip.current_color == self.sequence[self.current_sequence_index]:
                    print(f"Correct! That was number {self.current_sequence_index + 1} in the sequence")
                    self.score += 1
                    self.current_sequence_index += 1
                    if self.current_sequence_index == len(self.sequence):
                        print("\nSequence completed correctly! +2 bonus points")
                        self.score += 2
                else:
                    print(f"Wrong color! You shot {self.led_strip.current_color} but should have shot {self.sequence[self.current_sequence_index]}")
                    self.game_active = False
                    break
                self.shot_sensor.reset_shot()
            
            self.led_strip.turn_off()
            await asyncio.sleep(0.5)  # Brief pause between colors
        
    async def cycle_colors(self):
        self.start_time = time.time()
        sequence_length = 3  # Starting sequence length
        
        while self.game_active and time.time() - self.start_time < self.game_duration:
            # Generate and show new sequence
            self.generate_sequence(sequence_length)
            await self.show_sequence()
            print("\nNow repeat the sequence!")
            
            # Show random colors and check for shots
            await self.show_random_colors()
            
            if self.game_active and self.current_sequence_index == len(self.sequence):
                sequence_length += 1  # Increase sequence length for next round
        
        self.game_active = False
        self.led_strip.turn_off()
        print("\nGame Over!")
        print(f"Final score: {self.score}")

async def main():
    led_strip = LEDStrip()
    shot_sensor = ShotSensor()
    game = SimonSaysGame(led_strip, shot_sensor)
    
    print("\nWelcome to Simon Says!")
    print("Game will run for 1 minute")
    await asyncio.sleep(2)
    
    # Create tasks
    monitor_task = asyncio.create_task(shot_sensor.monitor_shots())
    color_cycle_task = asyncio.create_task(game.cycle_colors())
    
    try:
        print("Game starting in:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            await asyncio.sleep(1)
        print("GO!")
        
        # Wait for all tasks
        await asyncio.gather(monitor_task, color_cycle_task)
        
    except asyncio.CancelledError:
        led_strip.turn_off()
        await asyncio.sleep(1)
        print("Game cancelled!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGame stopped by user")
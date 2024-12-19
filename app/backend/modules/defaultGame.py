from modules.ledStrip import LEDStrip
from modules.shotSensor import ShotSensor
import asyncio

class DefaultGame:
    def __init__(self, led_strip: LEDStrip, shot_sensor: ShotSensor):
        print("Initializing Default Game...")  # Debug print
        self.led_strip = led_strip
        self.shot_sensor = shot_sensor
        self.score = 0
        self.game_active = True
        self.monitor_task = None
    
    async def start(self):
        """Start the shot monitoring"""
        if not self.monitor_task:
            self.monitor_task = asyncio.create_task(self.shot_sensor.monitor_shots())
    
    async def handle_shot(self):
        """Handle shot detection and update game state"""
        if self.shot_sensor.shot_detected:
            self.score += 1
            await self.celebrate_shot()
            self.shot_sensor.reset_shot()
    
    async def celebrate_shot(self):
        """Celebrate a successful shot with rainbow animation"""
        self.led_strip.rainbowCycle()
        self.led_strip.turn_off()  # Turn off LEDs after celebration
    
    def get_status(self) -> dict:
        """Get current game status"""
        status = {
            "status": "default_mode",
            "score": self.score,
            "sequence": [],
            "current_index": 0,
            "game_active": self.game_active,
            "current_color": self.led_strip.current_color
        }
        return status 
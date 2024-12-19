from modules.ledStrip import LEDStrip
from modules.shotSensor import ShotSensor

class DefaultGame:
    def __init__(self, led_strip: LEDStrip, shot_sensor: ShotSensor):
        self.led_strip = led_strip
        self.shot_sensor = shot_sensor
        self.score = 0
        self.game_active = True
    
    async def handle_shot(self):
        """Handle shot detection and update game state"""
        if self.shot_sensor.shot_detected:
            self.score += 1
            self.led_strip.rainbow(iterations=1)
            self.shot_sensor.reset_shot()
    
    def get_status(self) -> dict:
        """Get current game status"""
        return {
            "status": "default_mode",
            "score": self.score,
            "sequence": [],
            "current_index": 0,
            "game_active": self.game_active,
            "current_color": self.led_strip.current_color
        } 
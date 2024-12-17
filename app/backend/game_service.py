from typing import Optional
from modules.simonSays import SimonSaysGame
from modules.ledStrip import LEDStrip
from modules.shotSensor import ShotSensor

class GameService:
    _instance: Optional['GameService'] = None
    
    def __init__(self):
        self.led_strip = LEDStrip()
        self.shot_sensor = ShotSensor()
        self.current_game: Optional[SimonSaysGame] = None
    
    @classmethod
    def get_instance(cls) -> 'GameService':
        if cls._instance is None:
            cls._instance = GameService()
        return cls._instance
    
    def start_new_game(self) -> None:
        self.current_game = SimonSaysGame(self.led_strip, self.shot_sensor)
    
    def get_game_status(self) -> dict:
        if not self.current_game:
            return {"status": "no_game"}
        
        return {
            "score": self.current_game.score,
            "sequence": self.current_game.sequence,
            "current_index": self.current_game.current_sequence_index,
            "game_active": self.current_game.game_active,
            "current_color": self.led_strip.current_color
        }
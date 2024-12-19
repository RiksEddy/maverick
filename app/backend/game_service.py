from typing import Optional, Union
from modules.simonSays import SimonSaysGame
from modules.defaultGame import DefaultGame
from modules.ledStrip import LEDStrip
from modules.shotSensor import ShotSensor

class GameService:
    _instance: Optional['GameService'] = None
    
    def __init__(self):
        self.led_strip = LEDStrip()
        self.shot_sensor = ShotSensor()
        self.default_game = DefaultGame(self.led_strip, self.shot_sensor)
        self.simon_says_game: Optional[SimonSaysGame] = None
        self.current_game: Union[DefaultGame, SimonSaysGame] = self.default_game
    
    @classmethod
    def get_instance(cls) -> 'GameService':
        if cls._instance is None:
            cls._instance = GameService()
        return cls._instance
    
    async def start_new_game(self) -> None:
        self.simon_says_game = SimonSaysGame(self.led_strip, self.shot_sensor)
        self.current_game = self.simon_says_game
        await self.simon_says_game.start()
    
    def get_game_status(self) -> dict:
        return self.current_game.get_status()
    
    async def handle_game_loop(self) -> None:
        """Handle game loop for current game mode"""
        if isinstance(self.current_game, DefaultGame):
            await self.current_game.handle_shot()
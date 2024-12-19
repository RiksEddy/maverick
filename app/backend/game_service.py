from typing import Optional, Union
from modules.simonSays import SimonSaysGame
from modules.defaultGame import DefaultGame
from modules.ledStrip import LEDStrip
from modules.shotSensor import ShotSensor
import asyncio

class GameService:
    _instance: Optional['GameService'] = None
    
    def __init__(self):
        print("Initializing GameService...")  # Debug print
        self.led_strip = LEDStrip()
        self.shot_sensor = ShotSensor()
        self.default_game = DefaultGame(self.led_strip, self.shot_sensor)
        self.simon_says_game: Optional[SimonSaysGame] = None
        self.current_game: Union[DefaultGame, SimonSaysGame] = self.default_game
        print("GameService initialized")  # Debug print
    
    @classmethod
    async def initialize(cls) -> 'GameService':
        """Initialize the GameService and start the default game"""
        if cls._instance is None:
            cls._instance = GameService()
            # Start default game monitoring
            await cls._instance.default_game.start()
            print("Default game started")  # Debug print
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'GameService':
        if cls._instance is None:
            raise RuntimeError("GameService must be initialized with initialize() first")
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
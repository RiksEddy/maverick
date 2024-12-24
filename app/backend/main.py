from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

from game_service import GameService
from connection_manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    """Initialize the GameService when the application starts"""
    global game_service
    game_service = await GameService.initialize()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://ritishpi.local:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start-game")
async def start_game():
    game_service = GameService.get_instance()
    await game_service.start_new_game()
    return {"message": "Game started"}

@app.get("/game-status")
async def game_status():
    game_service = GameService.get_instance()
    return game_service.get_game_status()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            await game_service.handle_game_loop()
            status = game_service.get_game_status()
            await manager.broadcast(status)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

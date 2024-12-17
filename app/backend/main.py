from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

from game_service import GameService
from connection_manager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/start-game")
async def start_game():
    game_service = GameService.get_instance()
    game_service.start_new_game()
    return {"message": "Game started"}

@app.get("/game-status")
async def game_status():
    game_service = GameService.get_instance()
    return game_service.get_game_status()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    game_service = GameService.get_instance()
    
    try:
        while True:
            status = game_service.get_game_status()
            await manager.broadcast(status)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

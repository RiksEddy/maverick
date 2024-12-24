from fastapi import WebSocket
from typing import List
import asyncio
import json

class ConnectionManager:
    def __init__(self):
        print("ConnectionManager initialized")
        self.active_connections: List[WebSocket] = []
        print("ConnectionManager active connections:", self.active_connections)
    
    async def connect(self, websocket: WebSocket):
        print("ConnectionManager connect")
        await websocket.accept()
        print("ConnectionManager accepted websocket")
        self.active_connections.append(websocket)
        print("ConnectionManager active connections:", self.active_connections)
    
    async def disconnect(self, websocket: WebSocket):
        print("ConnectionManager disconnect")
        if websocket in self.active_connections:
            print("ConnectionManager disconnecting from websocket")
            self.active_connections.remove(websocket)
        print("ConnectionManager active connections:", self.active_connections)
    
    async def broadcast(self, message: dict):
        print("ConnectionManager broadcast")
        disconnected = []
        for connection in self.active_connections:
            print("ConnectionManager broadcasting to connection")
            try:
                await connection.send_json(message)
                print("ConnectionManager sent message to connection")
            except:
                disconnected.append(connection)
                print("ConnectionManager disconnected from connection")
        
        for connection in disconnected:
            await self.disconnect(connection)
            print("ConnectionManager disconnected from connection")
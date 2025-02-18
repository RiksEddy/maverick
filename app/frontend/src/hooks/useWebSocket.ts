import { useState, useEffect } from 'react';
import { GameStatus } from '../types/game';

export const useWebSocket = (url: string) => {
  const [connected, setConnected] = useState(false);
  const [gameStatus, setGameStatus] = useState<GameStatus | null>(null);

  useEffect(() => {
    let ws: WebSocket;
    
    const connect = () => {
      ws = new WebSocket(url);
      
      ws.onopen = () => {
        console.log('WebSocket connection established');
        setConnected(true);
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setGameStatus(data);
      };

      ws.onclose = (event) => {
        console.log('WebSocket connection closed:', event);
        setConnected(false);
        // Attempt to reconnect after 1 second
        setTimeout(connect, 1000);
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    };

    connect();

    return () => {
      ws.close();
    };
  }, [url]);

  return { connected, gameStatus };
};
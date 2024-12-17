import { useState } from 'react';
import { GameStatus } from '../types/game';

export const useGameControl = () => {
  const [error, setError] = useState<string | null>(null);

  const startGame = async () => {
    try {
      await fetch('http://rikseddypi.local:8000/start-game');
      const response = await fetch('http://rikseddypi.local:8000/game-status');
      const status: GameStatus = await response.json();
      return status;
    } catch (error) {
      setError('Failed to start game');
      console.error('Error starting game:', error);
    }
  };

  return { startGame, error };
};
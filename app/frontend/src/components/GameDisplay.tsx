import React from 'react';
import { GameStatus } from '../types/game';

interface GameDisplayProps {
  gameStatus: GameStatus;
}

export const GameDisplay: React.FC<GameDisplayProps> = ({ gameStatus }) => {
  return (
    <div className="space-y-6">
      <div className="text-2xl">Score: {gameStatus.score}</div>
      
      <div className={`w-32 h-32 rounded-full transition-colors duration-300 ${
        gameStatus.current_color === 'red' ? 'bg-red-500' :
        gameStatus.current_color === 'green' ? 'bg-green-500' :
        gameStatus.current_color === 'blue' ? 'bg-blue-500' :
        'bg-gray-700'
      }`} />
      
      {!gameStatus.game_active && (
        <div className="text-xl text-red-500">Game Over!</div>
      )}
    </div>
  );
};
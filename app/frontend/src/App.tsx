import { useWebSocket } from './hooks/useWebSocket';
import { useGameControl } from './hooks/useGameControl';
import { GameDisplay } from './components/GameDisplay';

function App() {
  const { connected, gameStatus } = useWebSocket('ws://rikseddypi.local:8000/ws');
  const { startGame, error } = useGameControl();

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Simon Says</h1>
        
        {error && (
          <div className="text-red-500 mb-4">{error}</div>
        )}
        
        {!connected && (
          <div className="text-yellow-500 mb-4">Connecting to game server...</div>
        )}
        
        {connected && !gameStatus && (
          <button
            onClick={startGame}
            className="bg-green-500 hover:bg-green-600 px-6 py-3 rounded-lg font-bold"
          >
            Start Game
          </button>
        )}
        
        {gameStatus && <GameDisplay gameStatus={gameStatus} />}
      </div>
    </div>
  );
}

export default App;

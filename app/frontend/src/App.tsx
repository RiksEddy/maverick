import { useWebSocket } from './hooks/useWebSocket';
import { useGameControl } from './hooks/useGameControl';
import { GameDisplay } from './components/GameDisplay';

function App() {
  const { connected, gameStatus } = useWebSocket('ws://192.168.254.92:8000/ws');
  const { startGame, error } = useGameControl();

  // Add this to debug the values
  console.log('WebSocket Status:', { connected, gameStatus });

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Project Maverick</h1>

        {/* Add this to debug
        <div className="mb-4 text-gray-400">
          Backend URL: {wsUrl}
          Connected: {String(connected)}
          Game Status: {JSON.stringify(gameStatus)}
        </div> */}
        
        {error && (
          <div className="text-red-500 mb-4">{error}</div>
        )}
        
        {!connected && (
          <div className="text-yellow-500 mb-4">Connecting to game server...</div>
        )}
        
        {gameStatus && <GameDisplay gameStatus={gameStatus} />}

        {connected && (gameStatus?.status === "no_game" || gameStatus?.status === "default_mode") && (
          <button
            onClick={startGame}
            className="bg-green-500 hover:bg-green-600 px-6 py-3 rounded-lg font-bold"
          >
            Start Game
          </button>
        )}
      </div>
    </div>
  );
}

export default App;

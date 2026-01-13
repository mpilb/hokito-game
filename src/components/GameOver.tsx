import type { Player } from '../types';

interface GameOverProps {
  winner: Player | 'draw' | null;
  blackScore: number;
  whiteScore: number;
  onNewGame: () => void;
}

const GameOver = ({ winner, blackScore, whiteScore, onNewGame }: GameOverProps) => {
  if (!winner) return null;

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-900 border border-accent/30 p-8 rounded-2xl shadow-2xl max-w-md w-full mx-4 text-center">
        <h2 className="text-3xl font-bold mb-6 text-blanc-creme">
          {winner === 'draw' ? 'ÉGALITÉ!' : winner === 'black' ? 'NOIR GAGNE!' : 'BLANC GAGNE!'}
        </h2>

        <div className="mb-6 flex justify-center gap-8">
          <div className="text-center">
            <div className="text-sm font-semibold mb-1 text-blanc-creme/60">NOIR</div>
            <div className={`text-4xl font-bold ${winner === 'black' ? 'text-accent' : 'text-gray-600'}`}>
              {blackScore}
            </div>
          </div>
          <div className="text-4xl font-bold text-blanc-creme/30">-</div>
          <div className="text-center">
            <div className="text-sm font-semibold mb-1 text-blanc-creme/60">BLANC</div>
            <div className={`text-4xl font-bold ${winner === 'white' ? 'text-accent' : 'text-gray-600'}`}>
              {whiteScore}
            </div>
          </div>
        </div>

        <button
          onClick={onNewGame}
          className="bg-accent hover:bg-accent/80 text-blanc-creme font-bold py-3 px-8 rounded-lg transition-all duration-200 hover:scale-105 shadow-lg"
        >
          Nouvelle Partie
        </button>
      </div>
    </div>
  );
};

export default GameOver;

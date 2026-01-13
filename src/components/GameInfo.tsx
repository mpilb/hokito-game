import type { Player } from '../types';

interface GameInfoProps {
  currentPlayer: Player;
  blackScore: number;
  whiteScore: number;
}

const GameInfo = ({ currentPlayer, blackScore, whiteScore }: GameInfoProps) => {
  return (
    <div className="mb-6 flex justify-between items-center">
      <div className="flex gap-8">
        <div className={`text-center p-4 rounded-lg ${currentPlayer === 'black' ? 'bg-noir text-blanc-creme ring-4 ring-accent' : 'bg-blanc-creme text-noir'} transition-all duration-300`}>
          <div className="text-sm font-semibold mb-1">NOIR</div>
          <div className="text-2xl font-bold">{blackScore}</div>
        </div>
        <div className={`text-center p-4 rounded-lg ${currentPlayer === 'white' ? 'bg-blanc-creme text-noir ring-4 ring-accent' : 'bg-fond-bois text-noir'} transition-all duration-300`}>
          <div className="text-sm font-semibold mb-1">BLANC</div>
          <div className="text-2xl font-bold">{whiteScore}</div>
        </div>
      </div>
      <div className="text-right">
        <div className="text-sm text-blanc-creme/60 mb-1">Tour actuel</div>
        <div className="text-xl font-bold text-blanc-creme">
          {currentPlayer === 'black' ? 'NOIR' : 'BLANC'}
        </div>
      </div>
    </div>
  );
};

export default GameInfo;

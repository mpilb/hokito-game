import type { Piece as PieceType } from '../types';

interface PieceProps {
  piece: PieceType;
  stackPosition: number;
  stackHeight: number;
}

const Piece = ({ piece, stackPosition }: PieceProps) => {
  const romanNumerals = { 1: 'I', 2: 'II', 3: 'III' };

  const offsetY = -stackPosition * 10;

  const bgColor = piece.color === 'black' ? 'bg-noir' : 'bg-blanc-creme';
  const textColor = piece.color === 'black' ? 'text-blanc-creme' : 'text-noir';
  const borderColor = piece.color === 'black' ? 'border-gray-700' : 'border-gray-300';

  return (
    <div
      className={`absolute w-full h-full rounded-full ${bgColor} ${textColor} ${borderColor} border-2 flex items-center justify-center font-bold text-lg shadow-lg transition-all duration-300`}
      style={{
        transform: `translateY(${offsetY}px)`,
        zIndex: stackPosition,
      }}
    >
      {romanNumerals[piece.value]}
    </div>
  );
};

export default Piece;

import type { Cell as CellType, Position } from '../types';
import Piece from './Piece';

interface CellProps {
  cell: CellType;
  position: Position;
  isSelected: boolean;
  isLegalMove: boolean;
  onClick: () => void;
}

const Cell = ({ cell, isSelected, isLegalMove, onClick }: CellProps) => {
  const hasStack = cell.pieces.length > 0;

  let bgColor = 'bg-fond-bois';
  if (isSelected) {
    bgColor = 'bg-accent';
  } else if (isLegalMove) {
    bgColor = 'bg-green-200';
  }

  return (
    <div
      className={`aspect-square ${bgColor} border border-accent rounded-lg relative cursor-pointer transition-all duration-200 hover:scale-105 hover:shadow-lg`}
      onClick={onClick}
    >
      {hasStack && (
        <div className="absolute inset-0 p-1">
          <div className="relative w-full h-full">
            {cell.pieces.map((piece, index) => (
              <Piece
                key={index}
                piece={piece}
                stackPosition={index}
                stackHeight={cell.pieces.length}
              />
            ))}
          </div>
        </div>
      )}
      {isLegalMove && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
        </div>
      )}
    </div>
  );
};

export default Cell;

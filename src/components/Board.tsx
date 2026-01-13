import type { Cell as CellType, Position } from '../types';
import Cell from './Cell';

interface BoardProps {
  board: CellType[][];
  selectedPosition: Position | null;
  legalMoves: Position[];
  onCellClick: (position: Position) => void;
}

const Board = ({ board, selectedPosition, legalMoves, onCellClick }: BoardProps) => {
  const isPositionSelected = (row: number, col: number) => {
    return selectedPosition?.row === row && selectedPosition?.col === col;
  };

  const isPositionLegalMove = (row: number, col: number) => {
    return legalMoves.some(move => move.row === row && move.col === col);
  };

  return (
    <div className="w-full max-w-[600px] mx-auto">
      <div className="grid grid-cols-6 gap-2 p-4 bg-blanc-creme rounded-xl shadow-2xl">
        {board.map((row, rowIndex) =>
          row.map((cell, colIndex) => (
            <Cell
              key={`${rowIndex}-${colIndex}`}
              cell={cell}
              position={{ row: rowIndex, col: colIndex }}
              isSelected={isPositionSelected(rowIndex, colIndex)}
              isLegalMove={isPositionLegalMove(rowIndex, colIndex)}
              onClick={() => onCellClick({ row: rowIndex, col: colIndex })}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Board;

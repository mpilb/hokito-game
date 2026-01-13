export type Player = 'black' | 'white';
export type PieceValue = 1 | 2 | 3;

export interface Piece {
  color: Player;
  value: PieceValue;
}

export interface Position {
  row: number;
  col: number;
}

export interface Cell {
  pieces: Piece[]; // pile de pièces, le dernier élément est le sommet
}

export interface GameState {
  board: Cell[][]; // 6x6
  currentPlayer: Player;
  selectedPosition: Position | null;
  legalMoves: Position[];
  gameOver: boolean;
  winner: Player | 'draw' | null;
}

export interface Direction {
  dr: number;
  dc: number;
}

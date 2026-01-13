import type { Cell, Piece, Player, PieceValue, Position, Direction } from './types';

// Initialiser le plateau avec placement aléatoire
export function initializeBoard(): Cell[][] {
  const board: Cell[][] = Array(6).fill(null).map(() =>
    Array(6).fill(null).map(() => ({ pieces: [] }))
  );

  // Créer les pièces pour chaque joueur
  const createPieces = (color: Player): Piece[] => {
    const pieces: Piece[] = [];
    // 6 pièces de chaque valeur (I, II, III)
    for (let i = 0; i < 6; i++) {
      pieces.push({ color, value: 1 as PieceValue });
      pieces.push({ color, value: 2 as PieceValue });
      pieces.push({ color, value: 3 as PieceValue });
    }
    return pieces;
  };

  // Mélanger un tableau (Fisher-Yates shuffle)
  const shuffle = <T,>(array: T[]): T[] => {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  };

  // Placer les pièces noires (rangées 0-2)
  const blackPieces = shuffle(createPieces('black'));
  let blackIndex = 0;
  for (let row = 0; row < 3; row++) {
    for (let col = 0; col < 6; col++) {
      board[row][col].pieces.push(blackPieces[blackIndex++]);
    }
  }

  // Placer les pièces blanches (rangées 3-5)
  const whitePieces = shuffle(createPieces('white'));
  let whiteIndex = 0;
  for (let row = 3; row < 6; row++) {
    for (let col = 0; col < 6; col++) {
      board[row][col].pieces.push(whitePieces[whiteIndex++]);
    }
  }

  return board;
}

// Vérifier si un joueur contrôle une case
export function isControlledBy(cell: Cell, player: Player): boolean {
  if (cell.pieces.length === 0) return false;
  return cell.pieces[cell.pieces.length - 1].color === player;
}

// Obtenir la valeur au sommet d'une pile
function getTopValue(cell: Cell): PieceValue | null {
  if (cell.pieces.length === 0) return null;
  return cell.pieces[cell.pieces.length - 1].value;
}

// Vérifier si une position est dans les limites du plateau
function isInBounds(pos: Position): boolean {
  return pos.row >= 0 && pos.row < 6 && pos.col >= 0 && pos.col < 6;
}

// Les 4 directions orthogonales
const DIRECTIONS: Direction[] = [
  { dr: -1, dc: 0 },  // haut
  { dr: 1, dc: 0 },   // bas
  { dr: 0, dc: -1 },  // gauche
  { dr: 0, dc: 1 }    // droite
];

// Explorer récursivement les mouvements possibles
function exploreMoves(
  board: Cell[][],
  currentPos: Position,
  remainingDistance: number,
  visitedPath: Position[],
  lastDirection: Direction | null,
  isSourceSingle: boolean
): Position[] {
  const validDestinations: Position[] = [];

  // Si on a parcouru toute la distance
  if (remainingDistance === 0) {
    // Vérifier si la destination est valide
    const cell = board[currentPos.row][currentPos.col];
    if (cell.pieces.length === 0) return []; // Case vide non permise

    const isDestSingle = cell.pieces.length === 1;

    // Règle cruciale : pièce seule → pièce seule, pile → pile
    if (isSourceSingle && isDestSingle) {
      return [currentPos];
    } else if (!isSourceSingle && !isDestSingle) {
      return [currentPos];
    }
    return [];
  }

  // Explorer les 4 directions
  for (const dir of DIRECTIONS) {
    // Si on a déjà une direction, on peut soit continuer tout droit, soit tourner à 90°
    if (lastDirection !== null) {
      const isSameDirection = dir.dr === lastDirection.dr && dir.dc === lastDirection.dc;
      const isOppositeDirection = dir.dr === -lastDirection.dr && dir.dc === -lastDirection.dc;

      // On ne peut pas faire demi-tour
      if (isOppositeDirection) continue;

      // Si on tourne à 90°, on doit être sur une case occupée
      if (!isSameDirection && remainingDistance === getTopValue(board[visitedPath[0].row][visitedPath[0].col])) {
        // On est encore à la position de départ, donc pas encore de virage possible
        continue;
      }
    }

    const nextPos: Position = {
      row: currentPos.row + dir.dr,
      col: currentPos.col + dir.dc
    };

    if (!isInBounds(nextPos)) continue;

    const nextCell = board[nextPos.row][nextPos.col];

    // On ne compte que les cases occupées
    if (nextCell.pieces.length === 0) {
      // Case vide : on la saute et on continue dans la même direction
      const jumpedMoves = exploreMoves(
        board,
        nextPos,
        remainingDistance, // Distance ne diminue pas
        [...visitedPath, nextPos],
        dir,
        isSourceSingle
      );
      validDestinations.push(...jumpedMoves);
    } else {
      // Case occupée : on diminue la distance
      const occupiedMoves = exploreMoves(
        board,
        nextPos,
        remainingDistance - 1,
        [...visitedPath, nextPos],
        dir,
        isSourceSingle
      );
      validDestinations.push(...occupiedMoves);
    }
  }

  return validDestinations;
}

// Calculer tous les coups légaux pour une position donnée
export function getLegalMoves(board: Cell[][], from: Position): Position[] {
  const cell = board[from.row][from.col];
  if (cell.pieces.length === 0) return [];

  const topValue = getTopValue(cell);
  if (topValue === null) return [];

  const isSourceSingle = cell.pieces.length === 1;

  // Explorer toutes les destinations possibles
  const destinations = exploreMoves(
    board,
    from,
    topValue,
    [from],
    null,
    isSourceSingle
  );

  // Supprimer les doublons
  const uniqueDestinations: Position[] = [];
  const seen = new Set<string>();

  for (const dest of destinations) {
    const key = `${dest.row},${dest.col}`;
    if (!seen.has(key) && (dest.row !== from.row || dest.col !== from.col)) {
      seen.add(key);
      uniqueDestinations.push(dest);
    }
  }

  return uniqueDestinations;
}

// Exécuter un coup et retourner le nouvel état
export function executeMove(board: Cell[][], from: Position, to: Position): Cell[][] {
  const newBoard = board.map(row =>
    row.map(cell => ({ pieces: [...cell.pieces] }))
  );

  // Prendre la pile source
  const sourcePieces = newBoard[from.row][from.col].pieces;

  // Ajouter la pile source au-dessus de la destination
  newBoard[to.row][to.col].pieces.push(...sourcePieces);

  // Vider la case source
  newBoard[from.row][from.col].pieces = [];

  return newBoard;
}

// Vérifier si un joueur peut jouer
export function canPlayerMove(board: Cell[][], player: Player): boolean {
  for (let row = 0; row < 6; row++) {
    for (let col = 0; col < 6; col++) {
      const cell = board[row][col];
      if (isControlledBy(cell, player)) {
        const moves = getLegalMoves(board, { row, col });
        if (moves.length > 0) {
          return true;
        }
      }
    }
  }
  return false;
}

// Calculer le score d'un joueur
export function calculateScore(board: Cell[][], player: Player): number {
  let score = 0;

  for (let row = 0; row < 6; row++) {
    for (let col = 0; col < 6; col++) {
      const cell = board[row][col];
      if (isControlledBy(cell, player)) {
        const topValue = getTopValue(cell);
        const stackSize = cell.pieces.length;
        if (topValue !== null) {
          score += topValue * stackSize;
        }
      }
    }
  }

  return score;
}

// Obtenir le gagnant et le score final
export function getWinner(board: Cell[][]): { winner: Player | 'draw', blackScore: number, whiteScore: number } {
  const blackScore = calculateScore(board, 'black');
  const whiteScore = calculateScore(board, 'white');

  let winner: Player | 'draw';
  if (blackScore > whiteScore) {
    winner = 'black';
  } else if (whiteScore > blackScore) {
    winner = 'white';
  } else {
    winner = 'draw';
  }

  return { winner, blackScore, whiteScore };
}

import { useState, useEffect } from 'react';
import type { GameState, Position, Cell, Player } from './types';
import {
  initializeBoard,
  getLegalMoves,
  executeMove,
  canPlayerMove,
  calculateScore,
  getWinner,
  isControlledBy,
} from './gameLogic';
import Board from './components/Board';
import GameInfo from './components/GameInfo';
import GameOver from './components/GameOver';
import Lobby from './components/Lobby';
import { MultiplayerProvider, useMultiplayer } from './MultiplayerContext';

function GameContent() {
  const {
    playerColor,
    opponentName,
    playerName,
    isGameStarted,
    makeMove,
    sendGameOver,
    requestNewGame,
    leaveRoom,
    roomCode
  } = useMultiplayer();

  const [showLobby, setShowLobby] = useState(true);
  const [gameState, setGameState] = useState<GameState>(() => ({
    board: initializeBoard(),
    currentPlayer: 'black',
    selectedPosition: null,
    legalMoves: [],
    gameOver: false,
    winner: null,
  }));

  // Écouter les coups de l'adversaire
  useEffect(() => {
    const handleOpponentMove = (event: any) => {
      const { newBoard, nextPlayer } = event.detail;
      setGameState({
        board: newBoard,
        currentPlayer: nextPlayer,
        selectedPosition: null,
        legalMoves: [],
        gameOver: false,
        winner: null,
      });
    };

    window.addEventListener('opponent-move', handleOpponentMove);
    return () => window.removeEventListener('opponent-move', handleOpponentMove);
  }, []);

  // Vérifier la fin de partie après chaque coup
  useEffect(() => {
    if (!gameState.gameOver && isGameStarted) {
      const canMove = canPlayerMove(gameState.board, gameState.currentPlayer);
      if (!canMove) {
        const result = getWinner(gameState.board);
        setGameState(prev => ({
          ...prev,
          gameOver: true,
          winner: result.winner,
        }));
        sendGameOver(result.winner, result.blackScore, result.whiteScore);
      }
    }
  }, [gameState.board, gameState.currentPlayer, gameState.gameOver, isGameStarted]);

  const handleCellClick = (position: Position) => {
    if (gameState.gameOver) return;

    // En multijoueur, vérifier que c'est le tour du joueur
    if (isGameStarted && gameState.currentPlayer !== playerColor) return;

    const cell = gameState.board[position.row][position.col];

    // Si on clique sur une destination légale
    const isLegalMove = gameState.legalMoves.some(
      move => move.row === position.row && move.col === position.col
    );

    if (isLegalMove && gameState.selectedPosition) {
      // Exécuter le coup
      const newBoard = executeMove(gameState.board, gameState.selectedPosition, position);
      const nextPlayer = gameState.currentPlayer === 'black' ? 'white' : 'black';

      setGameState({
        board: newBoard,
        currentPlayer: nextPlayer,
        selectedPosition: null,
        legalMoves: [],
        gameOver: false,
        winner: null,
      });

      // Envoyer le coup à l'adversaire
      if (isGameStarted) {
        makeMove(gameState.selectedPosition, position, newBoard, nextPlayer);
      }
    }
    // Si on clique sur une pièce qu'on contrôle
    else if (isControlledBy(cell, gameState.currentPlayer)) {
      const moves = getLegalMoves(gameState.board, position);
      setGameState(prev => ({
        ...prev,
        selectedPosition: position,
        legalMoves: moves,
      }));
    }
    // Si on clique ailleurs, désélectionner
    else {
      setGameState(prev => ({
        ...prev,
        selectedPosition: null,
        legalMoves: [],
      }));
    }
  };

  const handleNewGame = () => {
    const newBoard = initializeBoard();
    setGameState({
      board: newBoard,
      currentPlayer: 'black',
      selectedPosition: null,
      legalMoves: [],
      gameOver: false,
      winner: null,
    });

    if (isGameStarted) {
      requestNewGame(newBoard);
    }
  };

  const blackScore = calculateScore(gameState.board, 'black');
  const whiteScore = calculateScore(gameState.board, 'white');

  // Afficher le lobby si pas encore en jeu
  if (showLobby && !isGameStarted) {
    return <Lobby onStartGame={() => setShowLobby(false)} />;
  }

  const isMyTurn = gameState.currentPlayer === playerColor;
  const blackPlayerName = playerColor === 'black' ? playerName : opponentName;
  const whitePlayerName = playerColor === 'white' ? playerName : opponentName;

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <div className="flex items-center gap-4 mb-4">
        <h1 className="text-5xl font-bold text-blanc-creme tracking-wide">HOKITO</h1>
        {roomCode && (
          <div className="bg-accent text-blanc-creme px-4 py-2 rounded-lg font-bold text-sm">
            {roomCode}
          </div>
        )}
      </div>

      {isGameStarted && (
        <div className="mb-4 text-center">
          <p className="text-sm text-gris-fonce mb-1">
            {blackPlayerName} (Noir) vs {whitePlayerName} (Blanc)
          </p>
          <p className={`font-bold ${isMyTurn ? 'text-accent' : 'text-gris'}`}>
            {isMyTurn ? "C'est votre tour!" : "Tour de l'adversaire..."}
          </p>
        </div>
      )}

      <GameInfo
        currentPlayer={gameState.currentPlayer}
        blackScore={blackScore}
        whiteScore={whiteScore}
      />

      <Board
        board={gameState.board}
        selectedPosition={gameState.selectedPosition}
        legalMoves={gameState.legalMoves}
        onCellClick={handleCellClick}
      />

      <div className="flex gap-4 mt-8">
        <button
          onClick={handleNewGame}
          className="bg-accent hover:bg-accent/80 text-blanc-creme font-semibold py-2 px-6 rounded-lg transition-all duration-200 hover:scale-105 shadow-md"
        >
          Nouvelle Partie
        </button>
        {isGameStarted && (
          <button
            onClick={() => {
              leaveRoom();
              setShowLobby(true);
            }}
            className="bg-gris hover:bg-gris-fonce text-blanc-creme font-semibold py-2 px-6 rounded-lg transition-all duration-200 hover:scale-105 shadow-md"
          >
            Quitter
          </button>
        )}
      </div>

      {gameState.gameOver && (
        <GameOver
          winner={gameState.winner}
          blackScore={blackScore}
          whiteScore={whiteScore}
          onNewGame={handleNewGame}
        />
      )}
    </div>
  );
}

function App() {
  return (
    <MultiplayerProvider
      onOpponentMove={(from, to, newBoard, nextPlayer) => {
        // Cette fonction sera appelée par le contexte
        // On utilise un event custom pour mettre à jour le jeu
        window.dispatchEvent(new CustomEvent('opponent-move', {
          detail: { from, to, newBoard, nextPlayer }
        }));
      }}
      onGameStart={() => {
        console.log('Game started!');
      }}
      onOpponentDisconnected={() => {
        alert('Votre adversaire s\'est déconnecté');
      }}
      onJoinError={(error) => {
        alert(error);
      }}
    >
      <GameContent />
    </MultiplayerProvider>
  );
}

export default App;

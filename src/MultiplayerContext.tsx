import { createContext, useContext, useEffect, useState } from 'react';
import type { ReactNode } from 'react';
import { io, Socket } from 'socket.io-client';
import type { Cell, Player, Position } from './types';

interface MultiplayerContextType {
  socket: Socket | null;
  isConnected: boolean;
  roomCode: string | null;
  playerColor: Player | null;
  opponentName: string | null;
  playerName: string | null;
  isGameStarted: boolean;
  createRoom: (name: string) => void;
  joinRoom: (code: string, name: string) => void;
  makeMove: (from: Position, to: Position, newBoard: Cell[][], nextPlayer: Player) => void;
  sendGameOver: (winner: Player | 'draw', blackScore: number, whiteScore: number) => void;
  requestNewGame: (newBoard: Cell[][]) => void;
  leaveRoom: () => void;
}

const MultiplayerContext = createContext<MultiplayerContextType | null>(null);

export function useMultiplayer() {
  const context = useContext(MultiplayerContext);
  if (!context) {
    throw new Error('useMultiplayer must be used within MultiplayerProvider');
  }
  return context;
}

interface MultiplayerProviderProps {
  children: ReactNode;
  onOpponentMove?: (from: Position, to: Position, newBoard: Cell[][], nextPlayer: Player) => void;
  onGameStart?: (players: Array<{ id: string; name: string; color: Player }>) => void;
  onGameEnded?: (winner: Player | 'draw', blackScore: number, whiteScore: number) => void;
  onNewGameStarted?: (newBoard: Cell[][]) => void;
  onOpponentDisconnected?: () => void;
  onJoinError?: (error: string) => void;
}

export function MultiplayerProvider({
  children,
  onOpponentMove,
  onGameStart,
  onGameEnded,
  onNewGameStarted,
  onOpponentDisconnected,
  onJoinError
}: MultiplayerProviderProps) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [roomCode, setRoomCode] = useState<string | null>(() => {
    return localStorage.getItem('hokito_room_code');
  });
  const [playerColor, setPlayerColor] = useState<Player | null>(() => {
    const saved = localStorage.getItem('hokito_player_color');
    return saved as Player | null;
  });
  const [opponentName, setOpponentName] = useState<string | null>(null);
  const [playerName, setPlayerName] = useState<string | null>(() => {
    return localStorage.getItem('hokito_player_name');
  });
  const [isGameStarted, setIsGameStarted] = useState(false);

  useEffect(() => {
    // Use the same origin in production, localhost in development
    const serverUrl = import.meta.env.PROD
      ? window.location.origin
      : 'http://localhost:3000';

    const newSocket = io(serverUrl);

    newSocket.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);

      // Auto-reconnect if we have saved game data
      const savedRoomCode = localStorage.getItem('hokito_room_code');
      const savedPlayerName = localStorage.getItem('hokito_player_name');
      const savedPlayerColor = localStorage.getItem('hokito_player_color');

      if (savedRoomCode && savedPlayerName && savedPlayerColor) {
        console.log('Attempting auto-reconnect to room:', savedRoomCode);
        // Try to rejoin the existing room
        newSocket.emit('join-room', {
          roomCode: savedRoomCode,
          playerName: savedPlayerName
        });
      }
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server');
      setIsConnected(false);
    });

    newSocket.on('room-created', ({ roomCode, color, reconnected }) => {
      setRoomCode(roomCode);
      setPlayerColor(color);
      localStorage.setItem('hokito_room_code', roomCode);
      localStorage.setItem('hokito_player_color', color);
      if (reconnected) {
        console.log('Reconnected to existing room');
      }
    });

    newSocket.on('room-joined', ({ roomCode, color, reconnected }) => {
      setRoomCode(roomCode);
      setPlayerColor(color);
      localStorage.setItem('hokito_room_code', roomCode);
      localStorage.setItem('hokito_player_color', color);
      if (reconnected) {
        console.log('Reconnected to existing room');
      }
    });

    newSocket.on('opponent-reconnected', () => {
      console.log('Opponent has reconnected');
    });

    newSocket.on('game-start', ({ players }) => {
      setIsGameStarted(true);
      const opponent = players.find((p: any) => p.id !== newSocket.id);
      if (opponent) {
        setOpponentName(opponent.name);
      }
      onGameStart?.(players);
    });

    newSocket.on('opponent-move', ({ from, to, newBoard, nextPlayer }) => {
      onOpponentMove?.(from, to, newBoard, nextPlayer);
    });

    newSocket.on('game-ended', ({ winner, blackScore, whiteScore }) => {
      onGameEnded?.(winner, blackScore, whiteScore);
    });

    newSocket.on('new-game-started', ({ newBoard }) => {
      onNewGameStarted?.(newBoard);
    });

    newSocket.on('opponent-disconnected', () => {
      onOpponentDisconnected?.();
    });

    newSocket.on('join-error', (error) => {
      // If auto-reconnect failed, clear saved data
      const wasAutoReconnecting = localStorage.getItem('hokito_room_code');
      if (wasAutoReconnecting && error === 'Room not found') {
        console.log('Auto-reconnect failed: room no longer exists');
        localStorage.removeItem('hokito_room_code');
        localStorage.removeItem('hokito_player_color');
        setRoomCode(null);
        setPlayerColor(null);
      }
      onJoinError?.(error);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  const createRoom = (name: string) => {
    if (socket) {
      setPlayerName(name);
      localStorage.setItem('hokito_player_name', name);
      const savedRoomCode = localStorage.getItem('hokito_room_code');
      socket.emit('create-room', {
        playerName: name,
        existingRoomCode: savedRoomCode
      });
    }
  };

  const joinRoom = (code: string, name: string) => {
    if (socket) {
      setPlayerName(name);
      localStorage.setItem('hokito_player_name', name);
      socket.emit('join-room', { roomCode: code, playerName: name });
    }
  };

  const makeMove = (from: Position, to: Position, newBoard: Cell[][], nextPlayer: Player) => {
    if (socket && roomCode) {
      socket.emit('make-move', { roomCode, from, to, newBoard, nextPlayer });
    }
  };

  const sendGameOver = (winner: Player | 'draw', blackScore: number, whiteScore: number) => {
    if (socket && roomCode) {
      socket.emit('game-over', { roomCode, winner, blackScore, whiteScore });
    }
  };

  const requestNewGame = (newBoard: Cell[][]) => {
    if (socket && roomCode) {
      socket.emit('request-new-game', { roomCode, newBoard });
    }
  };

  const leaveRoom = () => {
    setRoomCode(null);
    setPlayerColor(null);
    setOpponentName(null);
    setIsGameStarted(false);
    // Clear saved game data
    localStorage.removeItem('hokito_room_code');
    localStorage.removeItem('hokito_player_color');
  };

  return (
    <MultiplayerContext.Provider
      value={{
        socket,
        isConnected,
        roomCode,
        playerColor,
        opponentName,
        playerName,
        isGameStarted,
        createRoom,
        joinRoom,
        makeMove,
        sendGameOver,
        requestNewGame,
        leaveRoom,
      }}
    >
      {children}
    </MultiplayerContext.Provider>
  );
}

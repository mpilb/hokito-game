import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const httpServer = createServer(app);

// Configure CORS based on environment
const allowedOrigins = process.env.NODE_ENV === 'production'
  ? [process.env.FRONTEND_URL || 'https://your-app.onrender.com']
  : ['http://localhost:5173', 'http://localhost:3000'];

const io = new Server(httpServer, {
  cors: {
    origin: allowedOrigins,
    methods: ["GET", "POST"],
    credentials: true
  }
});

// Serve static files from dist folder
app.use(express.static(join(__dirname, 'dist')));

// Catch-all middleware to serve index.html for client-side routing
app.use((req, res) => {
  res.sendFile(join(__dirname, 'dist', 'index.html'));
});

// Game rooms storage
const rooms = new Map();
const waitingPlayers = [];

// Generate random room code
function generateRoomCode() {
  return Math.random().toString(36).substring(2, 8).toUpperCase();
}

io.on('connection', (socket) => {
  console.log('Player connected:', socket.id);

  // Create a new game room
  socket.on('create-room', (playerName) => {
    const roomCode = generateRoomCode();
    const room = {
      code: roomCode,
      players: [{
        id: socket.id,
        name: playerName,
        color: 'black'
      }],
      gameState: null,
      started: false
    };

    rooms.set(roomCode, room);
    socket.join(roomCode);
    socket.emit('room-created', { roomCode, color: 'black' });
    console.log(`Room ${roomCode} created by ${playerName}`);
  });

  // Join an existing room
  socket.on('join-room', ({ roomCode, playerName }) => {
    const room = rooms.get(roomCode);

    if (!room) {
      socket.emit('join-error', 'Room not found');
      return;
    }

    if (room.players.length >= 2) {
      socket.emit('join-error', 'Room is full');
      return;
    }

    if (room.started) {
      socket.emit('join-error', 'Game already started');
      return;
    }

    room.players.push({
      id: socket.id,
      name: playerName,
      color: 'white'
    });

    socket.join(roomCode);
    socket.emit('room-joined', { roomCode, color: 'white' });

    // Notify both players that the game can start
    io.to(roomCode).emit('game-start', {
      players: room.players
    });

    room.started = true;
    console.log(`${playerName} joined room ${roomCode}`);
  });

  // Handle game moves
  socket.on('make-move', ({ roomCode, from, to, newBoard, nextPlayer }) => {
    const room = rooms.get(roomCode);
    if (!room) return;

    // Broadcast move to other player
    socket.to(roomCode).emit('opponent-move', {
      from,
      to,
      newBoard,
      nextPlayer
    });
  });

  // Handle game over
  socket.on('game-over', ({ roomCode, winner, blackScore, whiteScore }) => {
    const room = rooms.get(roomCode);
    if (!room) return;

    io.to(roomCode).emit('game-ended', {
      winner,
      blackScore,
      whiteScore
    });
  });

  // Handle new game request
  socket.on('request-new-game', ({ roomCode, newBoard }) => {
    const room = rooms.get(roomCode);
    if (!room) return;

    io.to(roomCode).emit('new-game-started', { newBoard });
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('Player disconnected:', socket.id);

    // Find and clean up rooms
    for (const [roomCode, room] of rooms.entries()) {
      const playerIndex = room.players.findIndex(p => p.id === socket.id);

      if (playerIndex !== -1) {
        // Notify other player
        socket.to(roomCode).emit('opponent-disconnected');

        // Remove room if game was in progress
        rooms.delete(roomCode);
        console.log(`Room ${roomCode} closed due to disconnection`);
        break;
      }
    }

    // Remove from waiting players
    const waitingIndex = waitingPlayers.findIndex(p => p.id === socket.id);
    if (waitingIndex !== -1) {
      waitingPlayers.splice(waitingIndex, 1);
    }
  });
});

const PORT = process.env.PORT || 3000;

httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

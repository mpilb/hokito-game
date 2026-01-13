# Hokito - Multiplayer Online Game

A real-time multiplayer strategy board game built with React, TypeScript, and WebSockets.

## Features

- **Real-time Multiplayer**: Play against friends online using WebSocket connections
- **Room System**: Create or join game rooms with unique codes
- **Strategic Gameplay**: Move stacks of pieces based on complex rules
- **Score Tracking**: Live score updates for both players
- **Modern UI**: Clean, responsive design with Tailwind CSS

## Tech Stack

- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Backend**: Node.js, Express, Socket.io
- **Real-time Communication**: WebSockets (Socket.io)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the project directory:
```bash
cd hokito-game
```

2. Install dependencies (already done if you see node_modules):
```bash
npm install
```

### Running the Game

You need to run **TWO** separate processes:

#### 1. Start the Backend Server (Terminal 1)

```bash
npm run server
```

This will start the WebSocket server on `http://localhost:3000`

#### 2. Start the Frontend Dev Server (Terminal 2)

```bash
npm run dev
```

This will start the Vite dev server on `http://localhost:5173`

### How to Play Multiplayer

1. **Player 1**:
   - Open `http://localhost:5173` in your browser
   - Enter your name
   - Click "Créer une nouvelle partie" (Create New Game)
   - Share the 6-character room code with your friend

2. **Player 2**:
   - Open `http://localhost:5173` in another browser window/tab (or on another device on the same network)
   - Enter your name
   - Enter the room code shared by Player 1
   - Click "Rejoindre la partie" (Join Game)

3. **Play**:
   - Player 1 (Black) goes first
   - Click on your pieces to see legal moves
   - Click on a highlighted destination to move
   - Players take turns automatically
   - Game ends when a player cannot move

## Game Rules

- **Board**: 6x6 grid
- **Pieces**: Each player has 18 pieces (6 of value I, II, and III)
- **Movement**: Move entire stacks based on the top piece's value
- **Special Rules**:
  - Single piece can only land on single piece
  - Stack can only land on stack
  - Pieces move orthogonally (not diagonally)
  - Empty spaces don't count toward movement distance
- **Scoring**: Value × Stack Height for all controlled stacks
- **Win Condition**: Highest score when opponent cannot move

## Building for Production

```bash
npm run build
```

This creates a `dist` folder with optimized production files.

## Development

- **Frontend code**: `src/` directory
- **Server code**: `server.js`
- **Game logic**: `src/gameLogic.ts`
- **Multiplayer context**: `src/MultiplayerContext.tsx`

## Troubleshooting

**Connection Issues:**
- Make sure both the server (port 3000) and dev server (port 5173) are running
- Check that no firewall is blocking the connections
- Ensure Socket.io client is connecting to the correct server URL

**Game Not Syncing:**
- Check browser console for errors
- Verify both players are in the same room
- Try refreshing the page and rejoining

## Future Enhancements

- [ ] Add chat functionality
- [ ] Implement spectator mode
- [ ] Add game replay feature
- [ ] Create ranked matchmaking
- [ ] Add sound effects
- [ ] Mobile-responsive improvements

## License

MIT

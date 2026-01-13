import { useState } from 'react';
import { useMultiplayer } from '../MultiplayerContext';

interface LobbyProps {
  onStartGame: () => void;
}

export default function Lobby({ onStartGame }: LobbyProps) {
  const {
    isConnected,
    roomCode,
    createRoom,
    joinRoom,
    isGameStarted
  } = useMultiplayer();

  const [playerName, setPlayerName] = useState('');
  const [joinCode, setJoinCode] = useState('');
  const [isWaiting, setIsWaiting] = useState(false);
  const [error, setError] = useState('');

  const handleCreateRoom = () => {
    if (!playerName.trim()) {
      setError('Please enter your name');
      return;
    }
    setError('');
    createRoom(playerName);
    setIsWaiting(true);
  };

  const handleJoinRoom = () => {
    if (!playerName.trim()) {
      setError('Please enter your name');
      return;
    }
    if (!joinCode.trim()) {
      setError('Please enter a room code');
      return;
    }
    setError('');
    joinRoom(joinCode.toUpperCase(), playerName);
  };

  const copyRoomCode = () => {
    if (roomCode) {
      navigator.clipboard.writeText(roomCode);
    }
  };

  if (isGameStarted) {
    onStartGame();
    return null;
  }

  if (isWaiting && roomCode) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="bg-gray-900/90 backdrop-blur-md rounded-2xl shadow-2xl p-8 max-w-md w-full border border-accent/30">
          <h2 className="text-3xl font-bold text-blanc-creme mb-6 text-center">En attente...</h2>

          <div className="bg-accent/10 border border-accent/20 rounded-xl p-6 mb-6">
            <p className="text-sm text-blanc-creme/60 mb-2 text-center">Code de la partie</p>
            <div className="flex items-center justify-center gap-3">
              <div className="text-4xl font-bold text-accent tracking-widest">
                {roomCode}
              </div>
              <button
                onClick={copyRoomCode}
                className="bg-accent hover:bg-accent/80 text-blanc-creme px-4 py-2 rounded-lg font-semibold transition-all duration-200 hover:scale-105"
              >
                Copier
              </button>
            </div>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center gap-2 text-blanc-creme/60">
              <div className="animate-pulse w-2 h-2 bg-accent rounded-full"></div>
              <div className="animate-pulse w-2 h-2 bg-accent rounded-full delay-75"></div>
              <div className="animate-pulse w-2 h-2 bg-accent rounded-full delay-150"></div>
            </div>
            <p className="mt-4 text-blanc-creme/80">
              En attente d'un adversaire...
            </p>
            <p className="mt-2 text-sm text-blanc-creme/40">
              Partagez le code avec votre ami
            </p>
          </div>

          <button
            onClick={() => setIsWaiting(false)}
            className="mt-6 w-full bg-gray-700 hover:bg-gray-600 text-blanc-creme font-semibold py-2 px-6 rounded-lg transition-all duration-200"
          >
            Annuler
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="bg-gray-900/90 backdrop-blur-md rounded-2xl shadow-2xl p-8 max-w-md w-full border border-accent/30">
        <h1 className="text-5xl font-bold text-blanc-creme mb-2 text-center tracking-wide">HOKITO</h1>
        <p className="text-center text-blanc-creme/60 mb-8">Multijoueur en ligne</p>

        {!isConnected && (
          <div className="bg-orange-900/50 border-l-4 border-orange-500 p-4 mb-6">
            <p className="text-orange-200">Connexion au serveur...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-900/50 border-l-4 border-red-500 p-4 mb-6">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        <div className="mb-6">
          <label className="block text-sm font-semibold text-blanc-creme/80 mb-2">
            Votre nom
          </label>
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            placeholder="Entrez votre nom"
            maxLength={20}
            className="w-full px-4 py-3 bg-gray-800 border-2 border-gray-700 text-blanc-creme rounded-lg focus:border-accent focus:outline-none transition-colors placeholder-gray-500"
            disabled={!isConnected}
          />
        </div>

        <button
          onClick={handleCreateRoom}
          disabled={!isConnected || !playerName.trim()}
          className="w-full bg-accent hover:bg-accent/80 disabled:bg-gray-700 disabled:cursor-not-allowed text-blanc-creme font-bold py-4 px-6 rounded-lg transition-all duration-200 hover:scale-105 shadow-lg mb-4"
        >
          Créer une nouvelle partie
        </button>

        <div className="flex items-center gap-4 my-6">
          <div className="flex-1 h-px bg-gray-700"></div>
          <span className="text-gray-500 font-semibold">OU</span>
          <div className="flex-1 h-px bg-gray-700"></div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-semibold text-blanc-creme/80 mb-2">
            Code de la partie
          </label>
          <input
            type="text"
            value={joinCode}
            onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
            placeholder="Entrez le code"
            maxLength={6}
            className="w-full px-4 py-3 bg-gray-800 border-2 border-gray-700 text-blanc-creme rounded-lg focus:border-accent focus:outline-none transition-colors uppercase tracking-widest text-center text-2xl font-bold placeholder-gray-500"
            disabled={!isConnected}
          />
        </div>

        <button
          onClick={handleJoinRoom}
          disabled={!isConnected || !playerName.trim() || !joinCode.trim()}
          className="w-full bg-transparent hover:bg-white/5 disabled:hover:bg-transparent disabled:opacity-50 text-blanc-creme font-bold py-4 px-6 rounded-lg transition-all duration-200 hover:scale-105 border-2 border-accent shadow-lg"
        >
          Rejoindre la partie
        </button>
      </div>
    </div>
  );
}

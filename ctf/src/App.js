import React, { useState, useEffect, useRef } from 'react';
import GameBoard from './GameBoard';
import Agent from './Agent';
import { io } from 'socket.io-client';
import agentRed from './redagent.png';
import agentBlue from './blueagent.png';

const agentImages = {
  'red': agentRed,
  'blue': agentBlue,
  // other colors
};

//const socket = io('http://128.97.30.83:8080');
const socket = io('http://localhost:8080');

function StartScreen({ onStart, onJoin, roomID }) {
  const [mode, setMode] = useState("random");
  const [inputRoomID, setInputRoomID] = useState("");
  const [waitingForPlayers, setWaitingForPlayers] = useState(false);

  const createRoom = () => {
    socket.emit('create_room', { mode: mode }); // Emit the create_room event to the server
  };

  const joinRoom = () => {
    socket.emit('join_room', { roomID: inputRoomID }); // Emit the join_room event to the server
  };

  // Listen for server to send room ID when creating a room
  useEffect(() => {
    socket.on('room_created', (data) => {
      onStart(mode, data.roomID);
      setWaitingForPlayers(true);
    });
    // Handle room join confirmation
    socket.on('join_confirmed', (data) => {
      onJoin(data.mode, data.roomID);
      setWaitingForPlayers(true);
    });
    // Handle start game
    socket.on('start-game', (data) => {
      setWaitingForPlayers(false);
    });
  }, [onStart, onJoin]);

  if (waitingForPlayers) {
    console.log('waiting for players')
    return <p>Waiting for players to join... ROOM: {roomID}</p>
  }

  return (
    <div>
      <input type="text" placeholder="Room ID" value={inputRoomID} onChange={e => setInputRoomID(e.target.value)} />
      <button onClick={joinRoom}>Join</button>
      <br />
      <select onChange={e => setMode(e.target.value)} value={mode}>
        <option value="random">Random</option>
        <option value="two-player">Two Player</option>
        <option value="four-player">Four Player</option>
      </select>
      <button onClick={createRoom}>Create</button>
    </div>
  );
}

const GameOverScreen = ({ onPlayAgain }) => (
  <div>
    <h1>Game Over!</h1>
    <button onClick={onPlayAgain}>Play again</button>
  </div>
);

const App = () => {
  const [agents, setAgents] = useState([]);
  const [obstacles, setObstacles] = useState([]);
  const [flags, setFlags] = useState([]);

  const [gameMode, setGameMode] = useState(null);
  const [gameRoom, setGameRoom] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);

  const gameRoomRef = useRef(null);


  const startGame = (mode, roomID) => {
    setGameMode(mode);
    setGameRoom(roomID);
    setGameStarted(false);
  }
  
  const joinGame = (mode, roomID) => {
    setGameMode(mode);
    setGameRoom(roomID);
    setGameStarted(false);
  }

  useEffect(() => {
    socket.on('start-game', () => {
      console.log('Game has started');
      setGameStarted(true);
    });

    socket.on('game-over', () => {
      console.log('Game is over');
      setGameOver(true);
    });
  }, []);

  useEffect(() => {
    gameRoomRef.current = gameRoom;
  }, [gameRoom]);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to server');
    }); 

    return () => {
      socket.disconnect();
    };

  }, []);
  
  const getAngle = (direction) => {
    const angle = parseInt(direction) * 90;
    return angle;
  };

  useEffect(() => {
    // The function to handle the "updateState" event
    const handleUpdateState = (message) => {
      console.log('update state received!')
      const parsedMessage = JSON.parse(message);

      console.log('update ID: ', parsedMessage.roomID);
      console.log('roomID: ', gameRoom);

      if (parsedMessage.roomID === gameRoom) {
        const {agent, obstacle, flag } = parsedMessage.state;

        console.log('Parsed agents:', agent);
        setAgents(agent || []);
        setObstacles(obstacle || []);
        setFlags(flag || []);
      }
    };

    // Add the event listener
    socket.on('updateState', handleUpdateState);

    // Remove the event listener when "gameRoom" changes or the component unmounts
    return () => {
      socket.off('updateState', handleUpdateState);
    };
  }, [gameRoom]);  // Dependencies

  // Add event listener only once, outside of any useEffect hooks
  useEffect(() => {
    const handleKeyDown = (e) => {
      console.log('key pressed: ', e.key)
      const keyToAction = {
        'w': 'forward',
        's': 'backward',
        'a': 'left',
        'd': 'right',
      };
  
      const action = keyToAction[e.key];
      if (action) {
        // Emit the action event to the server
        socket.emit('action', { action: action, room: gameRoomRef.current});
      }
    }

    document.addEventListener('keydown', (event) => handleKeyDown(event));

    return () => {
      document.removeEventListener('keydown', (event) => handleKeyDown(event));
    };
  }, [gameRoom]); // Add empty dependency array to run the effect only once

  useEffect(() => {
    document.body.style.overflow = 'hidden'; // prevent scrolling
  }, []);

  const middleX = window.innerWidth / 2;
  const middleY = window.innerHeight / 2;
  const rows = 10;
  const cols = 10;

  const playAgain = () => {
    setGameOver(false);
    setGameStarted(false);
  };

  if (!gameStarted) {
    console.log('displaying start screen!')
    return <StartScreen onStart={startGame} onJoin={joinGame} roomID={gameRoom} />;
  }
  else if (gameOver) {
    console.log('displaying game over screen!')
    return <GameOverScreen onPlayAgain={playAgain} />;
  }
  else{
    console.log('displaying game!')
    return (
      <div>
        {agents.length > 0 && obstacles.length > 0 && flags.length > 0 &&
          <GameBoard
            numRows={rows+2}
            numCols={cols+2}
            obstacleCoords={obstacles}
            agentCoords={agents}
            flagCoords={flags}
          />
        }       
        {agents.map(agent => {
          const agentImg = agentImages[agent.color];
          return (
            <Agent
              key={agent.id}
              id={agent.id}
              src={agentImg} // now this is dynamic based on the color of the agent
              position={{
                top: `${middleY - (rows/2 * 40) + 40 * agent.row + 25}px`,
                left: `${middleX - (cols/2 * 40) + 40 * agent.col + 20}px`
              }}
              direction={getAngle(agent.direction)}
            />
          );
        })}
      </div>
    );
  }
};

export default App;


import React, { useState, useEffect, useRef } from 'react';
import GameBoard from './GameBoard';
import { io } from 'socket.io-client';


const socket = io('http://128.97.30.83:8080');
//const socket = io('http://localhost:8080');

  // =======PREGAME DISPLAY=======
  function StartScreen({ onStart, onJoin, roomID }) {
  // game mode: default is random
  const [mode, setMode] = useState("random");
  const [inputRoomID, setInputRoomID] = useState("");

  // bool: are we waiting for other players or not?
  const [waitingForPlayers, setWaitingForPlayers] = useState(false);

  const createRoom = () => {
    socket.emit('create_room', { mode: mode }); // Emit the create_room event to the server
  };

  const joinRoom = () => {
    socket.emit('join_room', { roomID: inputRoomID }); // Emit the join_room event to the server
  };

  // Listen for server to send room creation/join and start events
  useEffect(() => {
    // handle room creation
    socket.on('room_created', (data) => {
      onStart(mode, data.roomID);
      setWaitingForPlayers(true);
    });
    // handle room join confirmation
    socket.on('join_confirmed', (data) => {
      onJoin(data.mode, data.roomID);
      setWaitingForPlayers(true);
    });
    // handle start game
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

  // =======GAME OVER DISPLAY=======
  const GameOverScreen = ({ onPlayAgain }) => (
  <div>
    <h1>Thanks for playing!</h1>
    <button onClick={onPlayAgain}>Play again</button>
  </div>
);

  // =======MAIN GAME DISPLAY=======
  const App = () => {
  const [socketId, setSocketId] = useState(null);

  const [grid, setGrid] = useState([])
  const [agents, setAgents] = useState([])

  // tracks active agents
  const [colorToID, setColorToID] = useState({})

  // game state variables: room, mode, status
  const [gameMode, setGameMode] = useState(null);
  const [gameRoom, setGameRoom] = useState(null);
  const [gameStarted, setGameStarted] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [visibility, setVisibility] = useState(false)
  const [color, setColor] = useState(null)
  
  const gameRoomRef = useRef(null);

  // =======BUTTON FUNCTIONS=======
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

  const playAgain = () => {
    setGameOver(false);
    setGameStarted(false);
  };

  // =======USEEFFECTS AND SOCKET EVENTS=======

  // handle connect/disconnect
  useEffect(() => {
    socket.on('connect', () => {
      setSocketId(socket.id);
      console.log('Connected to server');
    }); 

    return () => {
      socket.disconnect();
    };

  }, []);

  useEffect(() => {
    console.log('player colors', color);
  }, [color]);

  useEffect(() => {
    console.log('colortoid', colorToID);
  }, [colorToID]);

  useEffect(() => {
    console.log('visibility', visibility);
  }, [visibility]);

  // various socket events 
  useEffect(() => {
    socket.on('client_ids', (data) => {
      setColorToID(data)
    });

    socket.on('color-assign', (data)=> {
      setColor(data)
    });

    socket.on('vis-assign', (data) => {
      setVisibility(data)
    })

    socket.on('start-game', () => {
      console.log('Game has started');
      setGameStarted(true);
    });

    socket.on('game-over', () => {
      console.log('Game is over');
      setGameOver(true);
    });
  }, []);

  // store gameRoom as reference
  useEffect(() => {
    gameRoomRef.current = gameRoom;
  }, [gameRoom]);
  
  useEffect(() => {
    console.log('Updated grid:', grid);
  }, [grid]);

  useEffect(() => {
    console.log('agent dict:', agents);
  }, [agents]);

  // handles the "updateState" event
  useEffect(() => {
    const handleUpdateState = (message) => {
      console.log('update state received!')
      const parsedMessage = JSON.parse(message);
      
      console.log('update ID: ', parsedMessage.roomID);
      console.log('roomID: ', gameRoomRef.current);

      if (parsedMessage.roomID === gameRoomRef.current) {
        const gameGrid = parsedMessage.grid;
        const agentList = parsedMessage.agents;
        setGrid(gameGrid);
        setAgents(agentList)
      }
    };

    // Add the event listener
    socket.on('updateState', handleUpdateState);

    // Remove the event listener when "gameRoom" changes or the component unmounts
    return () => {
      socket.off('updateState', handleUpdateState);
    };
  }, [gameRoomRef]);

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
  }, [gameRoomRef]);

  useEffect(() => {
    document.body.style.overflow = 'hidden'; // prevent scrolling
  }, []);

  // =======RETURN=======

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
        {grid.length > 0 && agents.length > 0 &&
          <GameBoard
            grid = {grid}
            agents = {agents}
            fullVis = {visibility}
            activeAgentIds = {colorToID[gameRoomRef.current][socketId]}
            activeColors = {color[gameRoomRef.current][socketId]}
          />
        }       
      </div>
    );
  }
};

export default App;


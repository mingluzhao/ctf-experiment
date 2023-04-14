import React, { useState } from 'react';
import GameBoard from './GameBoard';
import { io } from "socket.io-client"

const socket = io('http://localhost:8080')
socket.on('connect', () => {
  console.log(socket.id);
});

socket.emit('state-to-server', {a1: (0,0)});

socket.on('state-to-client', (obj) => {
  console.log("client recieved message")
  console.log(obj);
})

const App = () => {

  // Set initial agent and obstacle coordinates
  const [agentCoords, setAgentCoords] = useState({ row: 9, col: 9 });
  const [obstacleCoords, setObstacleCoords] = useState([{ row: 4, col: 5 }, { row: 2, col: 2 }]);

  return (
    <div>
      {/* Render GameBoard component with agentCoords and obstacleCoords */}
      <GameBoard
        numRows={10} // Set the number of rows for the game board
        numCols={10} // Set the number of columns for the game board
        agentCoords={agentCoords} // Pass the agent coordinates to GameBoard
        obstacleCoords={obstacleCoords} // Pass the obstacle coordinates to GameBoard
      />
    </div>
  );
};

export default App;

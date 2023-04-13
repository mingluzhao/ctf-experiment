import React, { useState } from 'react';
import GameBoard from './GameBoard';
//import { io } from "socket.io-client"

const App = () => {
  //const socket = io('http://localhost:8080')

  const numRows=5;
  const numCols=5;
  // Set initial agent and obstacle coordinates
  const [agentCoords, setAgentCoords] = useState({ row: 2, col: 0 });
  const [obstacleCoords, setObstacleCoords] = useState([{ row: 0, col: 1 }, { row: 2, col: 2 }]);

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

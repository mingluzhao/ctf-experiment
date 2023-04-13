import React from 'react';
import GameBoard from './GameBoard';
import { io } from "socket.io-client"

const App = () => {
  const socket = io('http://localhost:8080')
  // Specify the agentCoords with the desired row and col values
  const agentCoords = {
    row: 4, // Specify the row index for the agent
    col: 3, // Specify the col index for the agent
  };
  const numRows=5;
  const numCols=5;

  return (
    <div>
      <h1>CTF</h1>
      {/* Render the GameBoard component and pass the agentCoords prop */}
      <GameBoard numRows={numRows} numCols={numCols} agentCoords={agentCoords} />
    </div>
  );
};

export default App;

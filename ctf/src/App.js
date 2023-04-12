import React from 'react';
import GameBoard from './GameBoard';

const App = () => {
  const numRows = 7; // Number of rows in the game board
  const numCols = 7; // Number of columns in the game board

  return (
    <div>
      <h1>Game Board</h1>
      <GameBoard numRows={numRows} numCols={numCols} /> {/* Render the GameBoard component */}
    </div>
  );
};

export default App;

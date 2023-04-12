// GameBoard.js

import React, { useState } from 'react';
import SquareParent from './SquareParent';
import Agent from './Agent'; // Import the Agent component

const GameBoard = ({ numRows, numCols, agentCoords }) => { // Accept numRows and numCols as props
  const [squares, setSquares] = useState([]);

  // Initialize the squares state with numRows x numCols empty objects
  useState(() => {
    const initialSquares = Array.from({ length: numRows }, () =>
      Array.from({ length: numCols }, () => ({}))
    );
    setSquares(initialSquares);
  }, [numRows, numCols]);

  // Callback function to update the state of a square
  const updateSquareState = (rowIndex, colIndex, newState) => {
    setSquares(prevSquares => {
      const newSquares = [...prevSquares];
      newSquares[rowIndex] = [...prevSquares[rowIndex]];
      newSquares[rowIndex][colIndex] = newState;
      return newSquares;
    });
  };

const renderSquares = () => {
  const squares = [];
  for (let row = 0; row < numRows; row++) {
    for (let col = 0; col < numCols; col++) {
      // Render the Agent component only in the square that matches the provided coordinates
      if (row === agentCoords.row && col === agentCoords.col) {
        squares.push(
          <div
            key={`${row}-${col}`}
            style={{ position: 'relative' }}
          >
            <SquareParent />
            <Agent style={{position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)'}} />
          </div>
        );
      } else {
        squares.push(
          <div
            key={`${row}-${col}`}
          >
            <SquareParent />
          </div>
        );
      }
    }
  }
  return squares;
};

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${numCols}, 40px)`,
        gridTemplateRows: `repeat(${numRows}, 40px)`,
        gap: '1px',
        // Add any additional styles for the game board, such as background color, border, etc.
      }}
    >
      {renderSquares()}
    </div>
  );
};

export default GameBoard;

import React, { useState } from 'react';
import SquareParent from './SquareParent';

const GameBoard = ({ numRows, numCols }) => {
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
        squares.push(<SquareParent key={`${row}-${col}`} />);
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
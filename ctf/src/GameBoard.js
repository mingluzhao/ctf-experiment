import React, { useState, useEffect } from 'react';
import SquareParent from './SquareParent';
import Agent from './Agent';
import agentImg from './agent.png';

const GameBoard = ({ numRows, numCols, agentCoords, obstacleCoords }) => {
  const [squares, setSquares] = useState([]);

  // Initialize the squares state with numRows x numCols empty objects
  useEffect(() => {
    const initialSquares = Array.from({ length: numRows }, () =>
      Array.from({ length: numCols }, () => ({}))
    );
    setSquares(initialSquares);
  }, [numRows, numCols]);

  const renderSquares = () => {
    const squares = [];
    for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
        // Render the Agent component only in the square that matches the provided coordinates
        if (row === agentCoords.row && col === agentCoords.col) {
          squares.push(
            <div key={`${row}-${col}`} style={{ position: 'relative' }}>
              <SquareParent agent={true} obstacle={false} flag={false} beam={false} />
              <Agent src={agentImg} />
            </div>
          );
        }
        // Render the Obstacle component for any square that matches the provided obstacle coordinates
        else if (obstacleCoords.some(coord => coord.row === row && coord.col === col)) {
          squares.push(
            <div key={`${row}-${col}`} style={{ position: 'relative' }}>
              {/* Pass obstacle prop as true to SquareParent component */}
              <SquareParent agent={false} obstacle={true} flag={false} beam={false} />
              <div className="obstacle"></div>
            </div>
          );
        } else {
          squares.push(
            <div key={`${row}-${col}`}>
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

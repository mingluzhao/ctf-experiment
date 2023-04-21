import React, { useState, useEffect } from 'react';
import SquareParent from './SquareParent';

const GameBoard = ({ numRows, numCols, obstacleCoords, agentCoords }) => {
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
        // Render the Obstacle component for any square that matches the provided obstacle coordinates
        if (obstacleCoords.some(coord => coord.row === row && coord.col === col)) {
          squares.push(
            <div key={`${row}-${col}`} style={{ position: 'relative' }}>
              {/* Pass obstacle prop as true to SquareParent component */}
              <SquareParent agent={false} obstacle={true} flag={false} beam={false} />
              <div className="obstacle"></div>
            </div>
          );
        // Render the Agent component for any square that matches the provided agent coordinates
        } else if (agentCoords.some(coord => coord.row === row && coord.col === col)) {
          squares.push(
            <div key={`${row}-${col}-agent`} style={{ position: 'relative' }}>
              {/* Pass agent prop as true to SquareParent component */}
              <SquareParent agent={true} obstacle={false} flag={false} beam={false} />
            </div>
          );
        } else {
          squares.push(
            <div key={`${row}-${col}`}>
              <SquareParent agent={false} obstacle={false} flag={false} beam={false}/>
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
        gap: '0px', // Change the gap to zero pixels
        // Add any additional styles for the game board, such as background color, border, etc.
      }}
    >
      {renderSquares()}
    </div>
  );
};

export default GameBoard;

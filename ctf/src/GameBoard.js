import React, { useState, useEffect } from 'react';
import SquareParent from './SquareParent';

import Agent from './Agent';
import agentRed from './redagent.png';
import agentBlue from './blueagent.png';

const agentImages = {
  'red': agentRed,
  'blue': agentBlue,
  // other colors
};

const GameBoard = ({ numRows, numCols, obstacleCoords, agentCoords, flagCoords, activePlayerTeam }) => {
  const [squares, setSquares] = useState([]);
  console.log(activePlayerTeam[0])
  // Initialize the squares state with numRows x numCols empty objects
  useEffect(() => {
    const initialSquares = Array.from({ length: numRows }, () =>
      Array.from({ length: numCols }, () => ({}))
    );
    setSquares(initialSquares);
  }, [numRows, numCols]);

  const isVisible = (row, col) => {
    for (let agent of agentCoords.filter(a => activePlayerTeam.includes(a.id))) {
      switch (agent.direction) {
        case 0: // up
          if (agent.row >= row && agent.row - row <= 2 && col > agent.col - 1 && col <= agent.col + 2) {
            return true;
          }
          break;
        case 1: // right
          if (agent.col + 2 <= col && col - agent.col - 2 <= 2 && row - 1 >= agent.row - 1 && row - 1 <= agent.row + 1) {
            return true;
          }
          break;
        case 2: // down
          if (agent.row <= row - 2 && row - agent.row - 2 <= 2 && col - 1 >= agent.col - 1 && col - 1 <= agent.col + 1) {
            return true;
          }
          break;
        case 3: // left
          if (agent.col >= col && agent.col - col <= 2 && row - 1 >= agent.row - 1 && row - 1 <= agent.row + 1) {
            return true;
          }
          break;
        default:
          break;
      }
    }
    return false;
  };

  const renderSquares = () => {
    const squares = [];
    for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
        const visible = isVisible(row, col);
        // Render the Obstacle component for any square that matches the provided obstacle coordinates
        if (obstacleCoords.some(coord => coord.row+1 === row && coord.col+1 === col)) {
          squares.push(
            <div key={`${row}-${col}`} style={{ position: 'relative' }}>
              {/* Pass obstacle prop as true to SquareParent component */}
              <SquareParent agent={false} obstacle={true} flag={false} beam={false} border={false} visible={visible}/>
            </div>
          );
        // Render the flag component for any square that matches the provided agent coordinates
        } else if (flagCoords.some(coord => coord.row+1 === row && coord.col+1 === col)) {
          squares.push(
            <div key={`${row}-${col}`} style={{ position: 'relative' }}>
              {/* Pass flag prop as true to SquareParent component */}
              <SquareParent agent={false} obstacle={false} flag={true} beam={false} border={false} visible={visible}/>
            </div>
          );
        } else if (row === 0 || row === numRows-1 || col === 0 || col === numCols-1) {
          squares.push(
            <div key={`${row}-${col}`} style={{ position: 'relative' }}>
              {/* Pass obstacle prop as true to SquareParent component */}
              <SquareParent agent={false} obstacle={false} flag={false} beam={false} border={true} visible={true}/>
            </div>
          );
        } else {
          squares.push(
            <div key={`${row}-${col}`}>
              <SquareParent agent={false} obstacle={false} flag={false} beam={false} border={false} visible={visible}/>
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
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Set the height of the container to fill the entire viewport
        // Add any additional styles for the container, such as background color, etc.
      }}
    >
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
    </div>
  );
};

export default GameBoard;

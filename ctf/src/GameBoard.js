import React from 'react';
import SquareParent from './SquareParent';
import Agent from './Agent';
import './GameBoard.css';

const GameBoard = ({ grid, agents, fullVis, activeAgentIds, activeColors}) => {

  const isVisible = (row, col) => {

    const adjustedRow = row - 1;
    const adjustedCol = col - 1;

    for (const id of activeAgentIds) {

      const agent = agents.find(a => a.id === id);
      const { direction, row: agentRow, col: agentCol } = agent;

      switch (direction) {
        case 0: // North
          if (adjustedCol >= agentCol - 1 && adjustedCol <= agentCol + 1 && adjustedRow <= agentRow - 1 && adjustedRow >= agentRow - 3) {
            return true;
          }
          break;
  
        case 1: // East
          if (adjustedRow >= agentRow - 1 && adjustedRow <= agentRow + 1 && adjustedCol >= agentCol + 1 && adjustedCol <= agentCol + 3) {
            return true;
          }
          break;
  
        case 2: // South
          if (adjustedCol >= agentCol - 1 && adjustedCol <= agentCol + 1 && adjustedRow >= agentRow + 1 && adjustedRow <= agentRow + 3) {
            return true;
          }
          break;
  
        case 3: // West
          if (adjustedRow >= agentRow - 1 && adjustedRow <= agentRow + 1 && adjustedCol <= agentCol - 1 && adjustedCol >= agentCol - 3) {
            return true;
          }
          break;
  
        default:
          break;
      }
    }
  
    return false;
  };

  const rows = grid.length;
  const cols = grid[0].length;

  console.log('Updated grid:', grid);
  console.log('agent dict:', agents);

  // Convert the 2D grid array to a flat array of SquareParent components
  const squares = grid.flatMap((row, i) =>
    row.map((cell, j) => {
      const [type, details = {}] = cell;
      let visible;
      if (fullVis){ visible = true; }
      else{ visible = isVisible(i, j) || type !== 'e'; }
      return <SquareParent key={`${i}-${j}`} type={type} details={details} visible={visible}/>;
    })
  );

  const filteredAgents = agents.filter(agent => {
    let visible;
    if (fullVis){ visible = true; }
    else{ visible = isVisible(agent.row + 1, agent.col + 1); }
    return activeColors.includes(agent.color) || visible;
  });
  
  console.log('Filtered agents:', filteredAgents);
  const agentComponents = filteredAgents.map(agent => (
    <Agent key={agent.id} agent={agent} />
  ));

  return (
    <div
      className="game-board"
      style={{
        gridTemplateRows: `repeat(${rows}, 1fr)`,
        gridTemplateColumns: `repeat(${cols}, 1fr)`,
      }}
    >
      {squares}
      {agentComponents}
    </div>
  );
};

export default GameBoard;
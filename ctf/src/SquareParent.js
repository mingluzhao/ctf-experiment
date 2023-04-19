import React, { useState } from 'react';
import './SquareParent.css';

const SquareParent = ({ agent, obstacle, flag, beam }) => {
  const [squareStates, setSquareStates] = useState({
    agent: agent,
    obstacle: obstacle,
    flag: flag,
    beam: beam
  });

  return (
    <div className="square">
      {squareStates.obstacle && (
        <div className="obstacle"></div>
      )}
      {/* Render additional elements or components based on the state of squareStates */}
      {squareStates.agent && (
        <div className="agent"></div>
      )}
    </div>
  );
};

export default SquareParent;

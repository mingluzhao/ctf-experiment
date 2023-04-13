import React, { useState } from 'react';
import './SquareParent.css';

const SquareParent = ({ obstacle, flag, beam }) => {
  // Initialize obstacle, flag, and beam states with props
  const [squareStates, setSquareStates] = useState({
    obstacle: obstacle,
    flag: flag,
    beam: beam
  });

  return (
    <div className="square">
      {squareStates.obstacle && (
        // Render obstacle only if obstacle state is true
        <div className="obstacle"></div>
      )}
      {/* Render additional elements or components based on the state of squareStates */}
    </div>
  );
};

export default SquareParent;

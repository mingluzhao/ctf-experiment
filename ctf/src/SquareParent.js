import React, { useState } from 'react';
import './SquareParent.css';

const SquareParent = () => {
  const [squareStates, setSquareStates] = useState({
    floor: false,
    wall: false,
    obstacle: false,
    flag: false,
    beam: false
  });

  return (
    <div className="square"></div>
  );
};

export default SquareParent;

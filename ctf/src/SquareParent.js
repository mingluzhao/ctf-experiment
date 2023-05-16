import React, { useState } from 'react';
import './SquareParent.css';
import flagImg from './flag.png';

const SquareParent = ({ agent, obstacle, flag, beam, border }) => {
  const [squareStates, setSquareStates] = useState({
    agent: agent,
    obstacle: obstacle,
    flag: flag,
    beam: beam,
    border: border
  });

  return (
    <div className="square">
      {squareStates.obstacle && (
        <div className="obstacle"></div>
      )}
      {squareStates.border && (
        <div className="border"></div>
      )}
      {squareStates.flag && (
        <img src={flagImg} className="flag" alt="Flag" />
      )}
    </div>
  );  
};

export default SquareParent;

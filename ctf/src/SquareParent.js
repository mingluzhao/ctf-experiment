import React, { useState } from 'react';
import './SquareParent.css';
import flagImg from './flag.png';

const SquareParent = ({ agent, obstacle, flag, beam, border, visible }) => {
  const [squareStates, setSquareStates] = useState({
    agent: agent,
    obstacle: obstacle,
    flag: flag,
    beam: beam,
    border: border
  });

  return (
    <div className={`square ${visible ? '' : 'non-visible'}`}>
      {visible && squareStates.obstacle && (
        <div className="obstacle"></div>
      )}
      {visible && squareStates.border && (
        <div className="border"></div>
      )}
      {visible && squareStates.flag && (
        <img src={flagImg} className="flag" alt="Flag" />
      )}
    </div>
  );  
};

export default SquareParent;

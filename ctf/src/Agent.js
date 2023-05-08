import React from 'react';
import PropTypes from 'prop-types';

const Agent = ({ src, position, direction }) => {
  const squareSize = 40;
  const halfSquareSize = squareSize / 2;
  const top = `calc(${position.top} - ${halfSquareSize}px)`;
  const left = `calc(${position.left} - ${halfSquareSize}px)`;
  const transform = `rotate(${direction}deg)`;
  
  return (
    <div style={{ position: 'absolute', top, left, transform }}>
      <img src={src} style={{ height: `${squareSize-5}px`, width: `${squareSize-5}px`, objectFit: "contain", border: "none" }} />
    </div>
  );
};

Agent.propTypes = {
  src: PropTypes.string.isRequired,
  position: PropTypes.shape({
    top: PropTypes.string.isRequired,
    left: PropTypes.string.isRequired,
  }).isRequired,
  direction: PropTypes.number.isRequired,
};  

export default Agent;

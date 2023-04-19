import React from 'react';
import PropTypes from 'prop-types';

const Agent = ({ src }) => {
    return (
      <div style={{ position: 'absolute', marginTop: '-40px' }}>
        <img src={src}
          style={{ height: "80%", width: "80%", objectFit: "contain" }}
        />
      </div>
    );
  };  

Agent.propTypes = {
  src: PropTypes.string.isRequired,
};

export default Agent;

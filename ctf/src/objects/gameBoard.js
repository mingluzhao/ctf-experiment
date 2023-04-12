import React from 'react';
import square from './square'

const gameBoard = (props) => {
    let size=20;
    {[...Array(size)].map(() => (
        <div>
          {[...Array(size)].map(() => (
            <square/>
          ))}
        </div>
    ))}
}

export default gameBoard
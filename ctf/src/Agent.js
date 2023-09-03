import React from 'react';
import './Agent.css';

import redagent from './assets/redagent.png'
import blueagent from './assets/blueagent.png'
import redagentflag from './assets/redagentflag.png'
import blueagentflag from './assets/blueagentflag.png'

const Agent = ({ agent }) => {
  console.log('passed filtered agents: ', agent)
  const directionMap = {
    0: 'north',
    1: 'east',
    2: 'south',
    3: 'west',
  };
  
  let agentImage;
  console.log(agent.hasflag)
  if(agent.hasflag === true){
    console.log('AGENT HAS FLAG')
    agentImage = agent.color === 'red' ? redagentflag : blueagentflag;
  }
  else if (agent.hasflag === false){
    console.log('AGENT DOESNT HAVE FLAG')    
    agentImage = agent.color === 'red' ? redagent : blueagent;
  }

  return (
    <img
      className={`agent ${directionMap[agent.direction]}`}
      src={agentImage}
      alt={`${agent.color} agent`}
      style={{
        position: 'absolute',
        gridRowStart: agent.row + 2,
        gridColumnStart: agent.col + 2,
      }}
    />
  );
};

export default Agent;
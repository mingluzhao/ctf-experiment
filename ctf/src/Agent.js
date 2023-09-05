import React from 'react';
import './Agent.css';

import redagent from './assets/redagent.png'
import blueagent from './assets/blueagent.png'
import redagentredflag from './assets/redagentredflag.png'
import blueagentredflag from './assets/blueagentredflag.png'
import redagentblueflag from './assets/redagentblueflag.png'
import blueagentblueflag from './assets/blueagentblueflag.png'

const Agent = ({ agent }) => {
  console.log('passed filtered agents: ', agent)
  const directionMap = {
    0: 'north',
    1: 'east',
    2: 'south',
    3: 'west',
  };
  
  let agentImage;
  console.log(agent.flagStatus)
  if(agent.flagStatus === null){
    console.log('AGENT DOESNT HAVE FLAG');
    agentImage = agent.color === 'red' ? redagent : blueagent;
  }
  else if (agent.flagStatus === 'red'){
    console.log('AGENT HAS RED FLAG');    
    agentImage = agent.color === 'red' ? redagentredflag : blueagentredflag;
  }
  else if (agent.flagStatus === 'blue'){
    console.log('AGENT HAS BLUE FLAG');    
    agentImage = agent.color === 'red' ? redagentblueflag : blueagentblueflag;
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
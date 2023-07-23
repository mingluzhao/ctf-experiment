import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import Agent from './Agent';
import { io } from 'socket.io-client';
import agentImg from './agent.png';

//const socket = io('http://128.97.30.83:8080');
const socket = io('http://localhost:8080');

const App = () => {
  const [agents, setAgents] = useState([]);
  const [obstacles, setObstacles] = useState([]);
  const [flags, setFlags] = useState([]);

  const [clientId, setClientId] = useState('');

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to server');
      
      setClientId(socket.id); // Set the client ID state when the socket connects      
    }); 

    // Listen for the "updateState" event, which is emitted when the server sends a state update
    socket.on('updateState', (message) => {
      console.log('Update state message:', message);
      const parsedMessage = JSON.parse(message);
      const {agent, obstacle, flag } = parsedMessage;
    
      console.log('Parsed agents:', agent);
      setAgents(agent || []);
      setObstacles(obstacle || []);
      setFlags(flag || []);
    });    


    return () => {
      socket.disconnect();
    };

  }, []);
  
  const getAngle = (direction) => {
    const angle = parseInt(direction) * 90;
    return angle;
  };

  // Add event listener only once, outside of any useEffect hooks
  useEffect(() => {
    const handleKeyDown = (e) => {
      console.log('key pressed: ', e.key)
      const keyToAction = {
        'w': 'forward',
        's': 'backward',
        'a': 'left',
        'd': 'right',
      };
  
      const action = keyToAction[e.key];
      if (action) {
        // Emit the action event to the server
        socket.emit('action', { action: action });
      }
    }

    document.addEventListener('keydown', (event) => handleKeyDown(event, clientId));

    return () => {
      document.removeEventListener('keydown', (event) => handleKeyDown(event, clientId));
    };
  }, []); // Add empty dependency array to run the effect only once

  useEffect(() => {
    document.body.style.overflow = 'hidden'; // prevent scrolling
  }, []);

  const middleX = window.innerWidth / 2;
  const middleY = window.innerHeight / 2;
  const rows = 10;
  const cols = 10;

  return (
    <div>
      {agents.length > 0 && obstacles.length > 0 && flags.length > 0 &&
        <GameBoard
          numRows={rows+2}
          numCols={cols+2}
          obstacleCoords={obstacles}
          agentCoords={agents}
          flagCoords={flags}
        />
      }       
      {agents.map(agent => (
        <Agent
          key={agent.id}
          id={agent.id}
          src={agentImg}
          position={{
            top: `${middleY - (rows/2 * 40) + 40 * agent.row + 25}px`,
            left: `${middleX - (cols/2 * 40) + 40 * agent.col + 20}px`
          }}
          direction={getAngle(agent.direction)}
        />
      ))}
    </div>
  );
};

export default App;

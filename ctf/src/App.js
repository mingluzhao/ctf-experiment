import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import Agent from './Agent';
import { io } from 'socket.io-client';
import agentImg from './agent.png';
import jsonMessage from './all_episode_trajectories.json';

const socket = io('http://localhost:8080');

socket.on('connect', () => {
  console.log('Connected to server');
});

const App = () => {
  const [agents, setAgents] = useState([]);
  const [obstacles, setObstacles] = useState([]);
  const [flags, setFlags] = useState([]);

  useEffect(() => {
    const intervalId = setInterval(() => {
      const message = jsonMessage;
      console.log('Received message:', message);
      if (!message) {
        return;
      }
  
      const agents = message.agent;
      const obstacles = message.obstacle;
      const flags = message.flag;
  
      const obstacleCoords = obstacles.map(o => ({ row: o.row, col: o.col }));
      const flagCoords = flags.map(f => ({ row: f.row, col: f.col }));
  
      setAgents(agents);
      setObstacles(obstacleCoords);
      setFlags(flagCoords);
    }, 1000); // interval in milliseconds
  
    return () => clearInterval(intervalId);
  }, []);
  

  useEffect(() => {
    agents.forEach(agent => {
      const agentImgElem = document.getElementById(agent.id);
      if (agentImgElem) {
        agentImgElem.style.transform = `rotate(${getAngle(agent.direction)}deg)`;
      }
    });
  }, [agents]);

  const getAngle = (direction) => {
    const angle = parseInt(direction) * 90;
    return angle;
  }  

  const handleKeyDown = (event) => {
    console.log("Key pressed")
    if (event.key === 'ArrowUp') {
      socket.emit('arrowKeyPress', { clientId: socket.id, direction: 'up' });
    } else if (event.key === 'ArrowDown') {
      socket.emit('arrowKeyPress', { clientId: socket.id, direction: 'down' });
    } else if (event.key === 'ArrowLeft') {
      socket.emit('arrowKeyPress', { clientId: socket.id, direction: 'left' });
    } else if (event.key === 'ArrowRight') {
      socket.emit('arrowKeyPress', { clientId: socket.id, direction: 'right' });
    }
  };

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    }
  }, []);

  return (
    <div>
      {agents.length > 0 && obstacles.length > 0 && flags.length > 0 &&
        <GameBoard
          numRows={10}
          numCols={10}
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
            top: `${40 * agent.row + 30}px`,
            left: `${40 * agent.col + 30}px`
          }}
          direction={getAngle(agent.direction)}
        />
      ))}
    </div>
  );
};

export default App;

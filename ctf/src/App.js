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
    }, 50); // interval in milliseconds
  
    return () => clearInterval(intervalId);
  }, []);

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

  useEffect(() => {
    document.body.style.overflow = 'hidden'; // prevent scrolling
  }, []);  

  const middleX = window.innerWidth / 2;
  const middleY = window.innerHeight / 2;
  const rows=15;
  const cols=15;

  return (
    <div>
      {agents.length > 0 && obstacles.length > 0 && flags.length > 0 &&
        <GameBoard
          numRows={rows}
          numCols={cols}
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

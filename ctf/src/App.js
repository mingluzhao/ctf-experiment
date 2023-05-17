import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import Agent from './Agent';
import { io } from 'socket.io-client';
import agentImg from './agent.png';
import jsonMessage from './all_episode_trajectories.json';

const socket = io('http://localhost:8080');

const App = () => {
  const [agents, setAgents] = useState([]);
  const [obstacles, setObstacles] = useState([]);
  const [flags, setFlags] = useState([]);
  const [clientId, setClientId] = useState('');
  const [IdInit, setIdInit] = useState(false);

  useEffect(() => {
    // Listen for the "connect" event, which is emitted when the socket connection is established
    socket.on('connect', () => {
      console.log('Connected to server');
      if (!IdInit) {
        setClientId(socket.id); // Set the client ID state when the socket connects
        setIdInit(true); // Set IdInit to true so that the clientId is not updated again
        socket.emit('addNewAgent', { clientId: socket.id });
        console.log("agent added" + socket.id);
      }
    });
  }, []);  

  useEffect(() => {
    const intervalId = setInterval(() => {
      const message = jsonMessage;
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

  const handleKeyDown = (event, clientId) => {
    event.preventDefault(); // prevent the default behavior of the event
  
    if (clientId === '') {
      return;
    }
    
    console.log("Key pressed")
    if (socket.id === clientId) {
      if (event.key === 'ArrowUp') {
        socket.emit('arrowKeyPress', { clientId: clientId, direction: 'up' });
      } else if (event.key === 'ArrowDown') {
        socket.emit('arrowKeyPress', { clientId: clientId, direction: 'down' });
      } else if (event.key === 'ArrowLeft') {
        socket.emit('arrowKeyPress', { clientId: clientId, direction: 'left' });
      } else if (event.key === 'ArrowRight') {
        socket.emit('arrowKeyPress', { clientId: clientId, direction: 'right' });
      }
    }
  };
  
  // Add event listener only once, outside of any useEffect hooks
  useEffect(() => {
    document.addEventListener('keydown', (event) => handleKeyDown(event, clientId));
  
    return () => {
      document.removeEventListener('keydown', (event) => handleKeyDown(event, clientId));
    }
  }, [clientId]); // Add empty dependency array to run the effect only once

  useEffect(() => {
    document.body.style.overflow = 'hidden'; // prevent scrolling
  }, []);  
  
  const middleX = window.innerWidth / 2;
  const middleY = window.innerHeight / 2;
  const rows=10;
  const cols=10;

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

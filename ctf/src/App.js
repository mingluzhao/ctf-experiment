import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import Agent from './Agent';
import { io } from 'socket.io-client';
import agentImg from './agent.png';

const socket = io('http://localhost:8080');

const App = () => {
  const [stateIndex, setStateIndex] = useState(0);
  const [agents, setAgents] = useState([]);
  const [obstacles, setObstacles] = useState([]);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    socket.emit('send-state-to-server');

    socket.on('send-state-to-client', (jsonMessage) => {
      const message = JSON.parse(jsonMessage);
      console.log('Received message:', message);

      setMessage(message[0]);
    });

    return () => {
      socket.off('send-state-to-client');
    }
  }, []);

  useEffect(() => {
    console.log('Parsing states');

    if (!message) {
      return;
    }

    const currentState = message[stateIndex];

    const agents = currentState[0].agent;
    const obstacles = currentState[0].obstacle;

    const obstacleCoords = obstacles.map(o => ({ row: o.row, col: o.col }));

    setAgents(agents);
    setObstacles(obstacleCoords);

    if (stateIndex < message.length - 1) {
      const timeoutId = setTimeout(() => {
        setStateIndex(stateIndex + 1);
      }, 1000);
      return () => clearTimeout(timeoutId);
    }
  }, [stateIndex, message]);

  useEffect(() => {
    agents.forEach(agent => {
      const agentImgElem = document.getElementById(agent.id);
      if (agentImgElem) {
        agentImgElem.style.transform = `rotate(${getAngle(agent.direction)}deg)`;
      }
    });
  }, [agents]);

  const getAngle = (direction) => {
    switch (direction) {
      case "up":
        return 0;
      case "down":
        return 180;
      case "left":
        return -90;
      case "right":
        return 90;
      default:
        return 0;
    }
  }

  const handleKeyDown = (event) => {
    const arrowKeys = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'];
    const directionMap = {
      'ArrowUp': 'up',
      'ArrowDown': 'down',
      'ArrowLeft': 'left',
      'ArrowRight': 'right',
    };
    if (arrowKeys.includes(event.key)) {
      const direction = directionMap[event.key];
      console.log(`Sending message with direction ${direction}`);
      socket.emit('arrow-key-pressed', { direction });
    }
  }

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    }
  });

  return (
    <div>
      {agents.length > 0 && obstacles.length > 0 &&
        <GameBoard
          numRows={10}
          numCols={10}
          obstacleCoords={obstacles}
          agentCoords={agents}
        />
      }
      {agents.map(agent => (
        <Agent
          key={agent.id}
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

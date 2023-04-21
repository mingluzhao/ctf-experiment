import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import Agent from './Agent';
import { io } from "socket.io-client"
import agentImg from "./agent.png"

const socket = io('http://localhost:8080');

const App = () => {

  const [agents, setAgents] = useState([]);
  const [obstacles, setObstacles] = useState([]);

  useEffect(() => {
    // Use socket.emit to send a request to the server
    socket.emit('send-state-to-server');

    // Listen for a message from the server
    socket.on('send-state-to-client', (jsonMessage) => {
      // Parse the JSON message
      const message = JSON.parse(jsonMessage);
      console.log('Received message:', message);

      // Access the agent and obstacles data from the parsed message
      const agents = message[0].agent;
      const obstacles = message[0].obstacle;

      // Convert obstacle array to an array of objects with row and col properties
      const obstacleCoords = obstacles.map(o => ({ row: o.row, col: o.col }));

      // Update the agents and obstacles state
      setAgents(agents);
      setObstacles(obstacleCoords);
    });

    // Clean up the socket event listener when component unmounts
    return () => {
      socket.off('send-state-to-client');
    }
  }, []);

  return (
    <div>
      {console.log(agents)}
      {console.log(obstacles)}
      {/* Render GameBoard component only if agents and obstacles are not empty */}
      {agents.length > 0 && obstacles.length > 0 &&
        <GameBoard
          numRows={10} // Set the number of rows for the game board
          numCols={10} // Set the number of columns for the game board
          obstacleCoords={obstacles} // Pass the obstacle coordinates to GameBoard
          agentCoords={agents}
        />
      }
      {/* Render Agent components for each agent in agents */}
      {agents.map(agent => (
        <Agent
          key={agent.id} // Assign a unique key to each Agent component
          src={agentImg}
          position={{
            top: `${40 * agent.row + 30}px`,
            left: `${40 * agent.col + 30}px`
          }}
        />
      ))}
    </div>
  );
};

export default App;

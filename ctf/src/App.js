import React, { useState, useEffect } from 'react';
import GameBoard from './GameBoard';
import { io } from "socket.io-client"

const socket = io('http://localhost:8080');

const App = () => {

  const [agentCoords, setAgentCoords] = useState(null);
  const [obstacleCoords, setObstacleCoords] = useState(null);

  useEffect(() => {
    // Use socket.emit to send a request to the server
    socket.emit('send-state-to-server');

    // Listen for a message from the server
    socket.on('send-state-to-client', (jsonMessage) => {
      // Parse the JSON message
      const message = JSON.parse(jsonMessage);
      console.log('Received message:', message);

      // Access the agent and obstacles data from the parsed message
      const agent = message[0].a1;
      const obstacles = message[0].o1;

      // Convert obstacleCoords object to an array of objects with row and col properties
      const obstacleCoordsArray = [{ row: obstacles.row, col: obstacles.col }];

      // Update the agent and obstacle coordinates in the state
      setAgentCoords(agent);
      setObstacleCoords(obstacleCoordsArray);
    });

    // Clean up the socket event listener when component unmounts
    return () => {
      socket.off('send-state-to-client');
    }
  }, []);
  console.log(obstacleCoords);
  return (
    <div>
      {/* Render GameBoard component only if agentCoords and obstacleCoords are not null */}
      {agentCoords && obstacleCoords &&
        <GameBoard
          numRows={10} // Set the number of rows for the game board
          numCols={10} // Set the number of columns for the game board
          agentCoords={agentCoords} // Pass the agent coordinates to GameBoard
          obstacleCoords={obstacleCoords} // Pass the obstacle coordinates to GameBoard
        />
      }
    </div>
  );
};

export default App;

const io = require("socket.io")(8080, {
    cors: {
        origin: ["http://localhost:3000", "http://localhost:3001"]
    },
});

io.on("connection", client => {
  client.emit('init', {data: 'hello world!'})

  console.log(client.id);

  client.on('send-state-to-server', () => {
    const jsonData = require('../all_episode_trajectories.json');
    const jsonString = JSON.stringify(jsonData);
    io.emit('send-state-to-client', jsonString);
  })

  client.on('arrow-key-pressed', (key) => {
    const message = {ID: client.id, direction: key.direction};
    console.log(JSON.stringify(message));
    io.emit('arrow-key-pressed', message);
  });
});
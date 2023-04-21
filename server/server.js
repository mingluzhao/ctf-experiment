const io = require("socket.io")(8080, {
    cors: {
        origin: ["http://localhost:3000", "http://localhost:3001"]
    },
});

io.on("connection", client => {
    client.emit('init', {data: 'hello world!'})

    console.log(client.id);

    client.on('send-state-to-server', () => {
        const jsonData = require('../all_episode_trajectories.json'); // Load the data from data.json
        //console.log('Loaded data from data.json:', jsonData); Add this line
        const jsonString = JSON.stringify(jsonData); // Stringify the JSON data
        io.emit('send-state-to-client', jsonString); // Emit the stringified JSON data
        console.log(jsonString);
    })
});


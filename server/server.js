const io = require("socket.io")(8080, {
    cors: {
        origin: ["http://localhost:3000"],
    },
});

io.on("connection", socket => {
    console.log(socket.id);
    socket.on('state-to-server', () => {
        const jsonData = require('./data.json'); // Load the data from data.json
        console.log('Loaded data from data.json:', jsonData); // Add this line
        const jsonString = JSON.stringify(jsonData); // Stringify the JSON data
        io.emit('state-to-client', jsonString); // Emit the stringified JSON data
        console.log(jsonString);
    })
});

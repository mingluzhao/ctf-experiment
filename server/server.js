const io = require("socket.io")(8080, {
    cors: {
        origin: ["http://localhost:3000"],
    },
});

io.on("connection", socket => {
    console.log(socket.id);
    socket.on('state-to-server', (obj) => {
        io.emit('state-to-client', {a1: (0,0)})
        console.log(obj);
    })
});




import socketio
import eventlet
from flask import Flask
from game import *

sio = socketio.Server(cors_allowed_origins='*')

client_order = {}
next_order_num = 0

game = Game(-1, 10)
init_json_string = json.dumps(game.state_dict)

with open('../ctf/src/all_episode_trajectories.json', 'w') as f:
    f.write(init_json_string)

@sio.on('connect')
def connect(sid, environ):
    global next_order_num
    # Store the client ID and order of arrival in the client_order map
    client_order[sid] = next_order_num
    next_order_num += 1
    print('Client', sid, 'connected (order', client_order[sid], ')')

@sio.on('arrowKeyPress')
def keydown(sid, data):
    print("key press detected")
    direction = data['direction']
    player_id = data['clientId']

    if direction == 'left':
        game.transition([client_order[player_id], "turn_l"])
    elif direction == 'right':
        game.transition([client_order[player_id], "turn_r"])
    elif direction == 'up':
        game.transition([client_order[player_id], "forward"])
    elif direction == 'down':
        game.transition([client_order[player_id], "backward"])
    
    json_string = json.dumps(game.state_dict)

    with open('../ctf/src/all_episode_trajectories.json', 'w') as f:
        f.write(json_string)
        print('wrote to file')


def main():
    app = socketio.WSGIApp(sio)
    print('Server started on port 8080')
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)


if __name__ == '__main__':
    main()
    # Start the server on port 5000

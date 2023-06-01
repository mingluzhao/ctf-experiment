import socketio
import eventlet
import json
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
    # Store the client ID and order of arrival in the client_order map
    print('Client', sid)

def emit_game_state():
    json_string = json.dumps(game.state_dict)
    with open('./all_episode_trajectories.json', 'w') as f:
        f.write(json_string)
    sio.emit('updateState', json_string)  # Emit the updated state to all clients

@sio.on('addNewAgent')
def addagent(sid, data):
    global next_order_num
    client_id = data['clientId']
    client_order[client_id] = next_order_num
    next_order_num += 1
    game.add_agent(client_id)
    print("Agent added with client ID: " + client_id)
    emit_game_state()

@sio.on('arrowKeyPress')
def keydown(sid, data):
    direction = data['direction']
    player_id = data['clientId']
    print(game.state_dict)
    if direction == 'left':
        game.transition([client_order[player_id], "turn_l"])
    elif direction == 'right':
        game.transition([client_order[player_id], "turn_r"])
    elif direction == 'up':
        game.transition([client_order[player_id], "forward"])
    elif direction == 'down':
        game.transition([client_order[player_id], "backward"])

    emit_game_state()

def main():
    app = socketio.WSGIApp(sio)
    print('Server started on port 8080')
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)

if __name__ == '__main__':
    main()
    # Start the server on port 5000

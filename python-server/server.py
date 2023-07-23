from game import Game  # The Game class you've implemented
import socketio
import eventlet
import json
import time
import threading
from constants import *

sio = socketio.Server(cors_allowed_origins="*")  # Allowing all origins for simplicity
app = socketio.WSGIApp(sio)

game = Game(-1, 10, init_state)

clients = []
client_to_agent = {}
actions = [None, None, None, None]

@sio.event
def connect(sid, environ):
    if len(client_to_agent) < 2:  # Only allow two clients
        client_to_agent[sid] = len(client_to_agent)
        sio.emit('assign_agent', {'agent_id': client_to_agent[sid]}, room=sid)
        print(f"Client {sid} connected and assigned agent {client_to_agent[sid]}")
        if len(client_to_agent) == 1:
            sio.start_background_task(game_loop)
    else:
        print("Connection attempt rejected. Maximum clients reached.")
        sio.disconnect(sid)

@sio.event
def action(sid, data):
    print('adding action!')
    agent_id = client_to_agent[sid]
    action = data['action']
    
    # Save the action if it's the first one received in the collection period
    if actions[agent_id] is None:
        actions[agent_id] = action

def game_loop():
    print("starting loop!")
    while True:
        # Let the agents move
        global actions
        print(actions)
        game.transition(actions)
        actions = [None, None, None, None]
        
        # Broadcast updated state to all clients
        print('emitting state')
        sio.emit('updateState', json.dumps(game.state_dict))
        
        # Wait for 0.5 seconds (the collection period)
        sio.sleep(0.5)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
    #eventlet.wsgi.server(eventlet.listen(('128.97.30.83', 8080)), app)

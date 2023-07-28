from game import Game  # The Game class you've implemented
import socketio
import eventlet
import json
import random
import time
import threading
from constants import *

sio = socketio.Server(cors_allowed_origins="*")  # Allowing all origins for simplicity
app = socketio.WSGIApp(sio)

next_room_id = 0

games = {}

client_to_room = {}
room_to_client = {}

client_to_agent = {}
actions = {}

clients = []

@sio.event
def connect(sid, environ):
     print(f"Client {sid} connected.")

@sio.event
def disconnect(sid):
    print("client ", sid, " disconnected")
    room = client_to_room.get(sid)
    if room:
        if sid in client_to_agent:
            del client_to_agent[sid]
        del client_to_room[sid]
        game = games.get(room)
        if game:
            # Check if there are no more clients in the room
            if not any(v == room for v in client_to_room.values()):
                del games[room]
                print(f"Room {room} deleted.")

@sio.event
def create_room(sid, data):
    global next_room_id
    roomID = str(next_room_id)
    mode = data['mode']
    next_room_id += 1

    #create the room
    sio.enter_room(sid, roomID)

    client_to_room[sid] = roomID
    room_to_client[roomID] = [sid]

    #create instance of Game
    if mode == 'random':
        maxclient = 1
    elif mode == 'two-player':
        maxclient = 2
    elif mode == 'four-player':
        maxclient = 4

    game = Game(-1, 10, init_state)

    games[roomID] = game, maxclient
    actions[roomID] = [None, None, None, None]

    print("created room with ID ", roomID)
    sio.emit('room_created', {'roomID': roomID}, room=sid)

    if mode == 'random':
        sio.emit('start-game', room=roomID) # Emit start-game to the room
        sio.start_background_task(game_loop, roomID) 
    else:
        client_to_agent[sid] = 0
        print('client controlling agent: ', 0)

@sio.event
def join_room(sid, data):
    roomID = data['roomID']
    maxclients = games[roomID][1]
    # Check if room exists and has space
    if roomID in games and len(room_to_client[roomID]) < maxclients:
        sio.enter_room(sid, roomID)

        client_to_agent[sid] = len(room_to_client[roomID])
        print('client controlling agent: ', len(room_to_client[roomID]))

        client_to_room[sid] = roomID
        room_to_client[roomID].append(sid)

        print("joined room with ID ", roomID)
        sio.emit('join_confirmed', {'roomID': roomID, 'mode': games[roomID][1]}, room=sid)

        if len(room_to_client[roomID]) == maxclients:
            sio.emit('start-game', room=roomID)  # Emit start-game to the room
            sio.start_background_task(game_loop, roomID) 
    else:
        sio.emit('join_rejected', {'roomID': roomID}, room=sid)

@sio.event
def action(sid, data):
    if sid not in client_to_agent:
        return

    print('adding action!')
    agent_id = client_to_agent[sid]

    room = data['room']
    action = data['action']

    print(room, action)
    
    # Save the action if it's the first one received in the collection period
    if actions[room][agent_id] is None:
        actions[room][agent_id] = action

def game_loop(roomID):
    game, maxclient = games[roomID]

    if maxclient == 1:
        num_random = 4
    elif maxclient == 2:
        num_random = 2
    elif maxclient == 4:
        num_random = 0

    print("starting loop!")
    while True:
        # Let the agents move
        global actions

        rand_actions = [random.choice(['forward', 'backward', 'left', 'right']) for i in range(num_random)]

        actions[roomID][(4 - num_random):] = rand_actions
        game.transition(actions[roomID])
        actions[roomID] = [None, None, None, None]
        
        # Broadcast updated state to all clients
        print('emitting state')
        sio.emit('updateState', json.dumps({'roomID': roomID, 'state': game.state_dict}),  room = roomID)
        
        # Wait for 0.5 seconds (the collection period)
        sio.sleep(0.5)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
    #eventlet.wsgi.server(eventlet.listen(('128.97.30.83', 8080)), app)

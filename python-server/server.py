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
gamestatus = {}

client_to_room = {}
room_to_client = {}

client_to_agent = {}
actions = {}

clients = []

@sio.event
def connect(sid, environ):
     print(f"Client {sid} connected.")

def cleanup_game(roomID):
    # delete associated game
    del games[roomID]

    # delete client -> room connections
    for k in list(client_to_room.keys()):
        if client_to_room[k] == roomID:
            del client_to_room[k]
    
    # delete room -> client connections
    del room_to_client[roomID]

    # delete client -> agent connections
    if roomID in client_to_agent:
        del client_to_agent[roomID]

@sio.event
def disconnect(sid):
    print("client ", sid, " disconnected")
    #check if client was part of a room
    roomID = client_to_room.get(sid)
    if roomID:
        #remove client from room/agent storage lists
        if client_to_agent.get(roomID) and sid in client_to_agent[roomID]:
            del client_to_agent[roomID][sid]
        del client_to_room[sid]
        room_to_client[roomID].remove(sid)

        #check if the room is now empty   
        if len(room_to_client[roomID]) == 0:
            gamestatus[roomID] = 'ended'
            print('status of game ', roomID, ': ', gamestatus[roomID])


@sio.event
def create_room(sid, data):
    # generate roomID, get game mode
    global next_room_id
    roomID = str(next_room_id)
    mode = data['mode']
    next_room_id += 1

    # create the room
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
    gamestatus[roomID] = 'pending'

    games[roomID] = game, maxclient
    actions[roomID] = [None, None, None, None]

    print("created room with ID ", roomID)
    sio.emit('room_created', {'roomID': roomID}, room=sid)

    if mode == 'random':
        sio.emit('start-game', room=roomID) # Emit start-game to the room
        gamestatus[roomID] = 'running'
        sio.start_background_task(game_loop, roomID)
    else:
        client_to_agent[roomID] = {}
        client_to_agent[roomID][sid] = 0
        print('client controlling agent: ', 0)

@sio.event
def join_room(sid, data):
    # extract roomID
    roomID = data['roomID']

    #check if room exists
    if roomID not in games:
        sio.emit('join_rejected', {'roomID': roomID}, room=sid)

    # get game mode
    maxclients = games[roomID][1]

    # check if room exists and has space, and the game hasn't started
    if len(room_to_client[roomID]) < maxclients and gamestatus[roomID] == 'pending':
        sio.enter_room(sid, roomID)

        client_to_agent[roomID][sid] = len(room_to_client[roomID])
        print('client controlling agent: ', len(room_to_client[roomID]))

        client_to_room[sid] = roomID
        room_to_client[roomID].append(sid)

        print("joined room with ID ", roomID)
        sio.emit('join_confirmed', {'roomID': roomID, 'mode': games[roomID][1]}, room=sid)

        if len(room_to_client[roomID]) == maxclients:
            sio.emit('start-game', room=roomID)  # Emit start-game to the room
            gamestatus[roomID] = 'running'
            sio.start_background_task(game_loop, roomID) 
    else:
        sio.emit('join_rejected', {'roomID': roomID}, room=sid)

@sio.event
def action(sid, data):
    # extract roomID and action
    
    roomID = data['room']
    action = data['action']

    # if game not running, return
    if gamestatus[roomID] != 'running':
        return 
    # if this is a random game, return
    if sid not in client_to_agent[roomID]:
        return

    # get ID of agent to be moved
    # print('adding action!')
    agent_id = client_to_agent[roomID][sid]
    # print(roomID, action)
    
    # Save the action if it's the first one received in the collection period
    if actions[roomID][agent_id] is None:
        actions[roomID][agent_id] = action

def game_loop(roomID):
    
    # extract game
    game, maxclient = games[roomID]

    # get number of random agents
    if maxclient == 1:
        num_random = 4
    elif maxclient == 2:
        num_random = 2
    elif maxclient == 4:
        num_random = 0

    print("starting loop!")
    while gamestatus[roomID] == 'running':
        print('gamestatus: ', gamestatus[roomID])
        # Let the agents move
        global actions

        # generate random actions
        rand_actions = [random.choice(['forward', 'backward', 'left', 'right']) for i in range(num_random)]
        actions[roomID][(4 - num_random):] = rand_actions

        # transition and reset actions
        game.transition(actions[roomID])
        actions[roomID] = [None, None, None, None]
        
        # Broadcast updated state to all clients
        sio.emit('updateState', json.dumps({'roomID': roomID, 'state': game.state_dict}),  room = roomID)
        
        # Check if the game is over, cleanup if so
        if game.is_terminal():
            print('game over')
            sio.emit('game-over', room=roomID)
            gamestatus[roomID] = 'ended'
            break
        # Wait for 0.5 seconds (the collection period)
        sio.sleep(0.5)
    
    # delete associated game
    del games[roomID]
    del gamestatus[roomID]

    # delete client -> room connections
    for k in list(client_to_room.keys()):
        if client_to_room[k] == roomID:
            del client_to_room[k]
    
    # delete room -> client connections
    del room_to_client[roomID]

    # delete client -> agent connections
    if roomID in client_to_agent:
        del client_to_agent[roomID]
    
    print("client_to_room: ", client_to_room)
    print("room_to_client: ", room_to_client)
    print("client_to_agent: ", client_to_agent)
    print("games: ", games)
    print("gamestatus: ", gamestatus)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8080)), app)
    #eventlet.wsgi.server(eventlet.listen(('128.97.30.83', 8080)), app)

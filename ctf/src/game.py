import random 
import json 

grid_size = 10

class State: # each state stores the positions, reward, action, and terminal status
    def __init__(self, agent_position, obstacle_position, flag_position):
        self.state_dict = {
            "a1": agent_position,
            "o1": obstacle_position,
            "f1": flag_position
        }
        self.reward = { # default reward is 0
            'a1': 0
        }
        self.action = { # default action is not moving
            'a1': 0
        }
        self.terminal = False

    def policy_random(state): 
        agent_actions = []
        possible_moves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)] 
        agent_position = state.state_dict['a1'] # take coord of agent from state dictionary
        
        for move in possible_moves: 
            # calculate the new position of the agent by adding the move to the agent's current position
            new_pos = (agent_position[0] + move[0], agent_position[1] + move[1])
        
            #check if the new position is outside the grid or collides with an obstacle
            if (new_pos[0] < 0 or new_pos[0] >= grid_size or
                new_pos[1] < 0 or new_pos[1] >= grid_size or 
                new_pos == state.state_dict['o1']): 
                # if the new position is invalid, skip this move 
                continue
            # if the new position is valid, add move to the agents_action list 
            agent_actions.append(move)
        # add an action to agent_actions for every agent in state
        return agent_actions  # returns a new state from agents movement 
    
    def transition(state, agent_action):
        new_state = state.copy()
        #update all the agent coordinates in the state
        return new_state
    
    def reward(state, action):
        # how is reward calculated? not sure what -action_cost means
        return 0

# generates a random initial state for the envrioment 
state = State((random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)),
              (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)),
              (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)))

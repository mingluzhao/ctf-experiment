import random 
import json 

grid_size = 10

# OUTPUT : trajectory - json file - a numpy array as the output 
# have a function that changes the numpy array to a json file 

# class should be called game 
# for the initialization you have the state 
# intialization should take care of the random state section 

class Game: # each state stores the positions, reward, action, and terminal status
    def __init__(self, agent_positions, obstacle_positions, flag_position, action_cost, goal_reward):
        self.state_dict = {
            "a1": agent_positions,
            "o1": obstacle_positions,
            "f1": flag_position
        }
        self.reward = { # default reward is 0
            'a1': 0
        }
        self.action = { # default action is not moving
            'a1': 0
        }
        self.action_cost = action_cost 
        self.goal_reward = goal_reward
        self.terminal = False
        

    # just be inputing the state and return the action 
    # policy random , random choice 
    # returns the ones thats chosen 

    def policy_random(state): 
        agent_actions = []
        possible_moves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)] 
        # agent_position = state.state_dict['a1'] # take coord of agent from state dictionary

        # return a random action from the list of valid actions
        return random.choice(possible_moves)

    
    def transition(state, agent_actions):
        new_state = state.copy()
        #update all the agent coordinates in the state

            
        return new_state
    
    def reward(state, action):
        # how is reward calculated? not sure what -action_cost means
        # action cost should be dependent on what action you take 
        # one exception , when agents gets to goal -> define where the flag is 
        return 0
    
    # checking weather the agent has captured the flag or gotten to the goal 
    def is_terminal(state): 
        terminal = False
        for agent_pos in state.state_dict["a1"]:
            if agent_pos == state.state_dict["f1"]:
                terminal = true
        return terminal 
    # get to the flag, getting a winning bonus -


# generates a random initial state for the envrioment 
state = Game((random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)),
              (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)),
              (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)))

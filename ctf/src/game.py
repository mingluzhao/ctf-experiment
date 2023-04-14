import random 
import copy
import json 

grid_size = 10

# OUTPUT : trajectory - json file - a numpy array as the output 
# have a function that changes the numpy array to a json file 

# class should be called game 
# for the initialization you have the state 
# intialization should take care of the random state section 

class Game: # each state stores the positions, reward, action, and terminal status
    def __init__(self, agent_count, obstacle_count, flag_count, action_cost, goal_reward):
        self.state_dict = {
            "a1": (random.randint(0, 9), random.randint(0, 9)),
            "o1": (random.randint(0, 9), random.randint(0, 9)),
            "f1": (random.randint(0, 9), random.randint(0, 9))
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
        agent_actions = random.choice(possible_moves)
        return agent_actions
    
    def transition(state, agent_actions):
        print(state)
        print(type(state))
        new_state = copy.deepcopy(state)
        new_state = list(new_state)
        #update all the agent coordinates in the state
        new_agent_positions = []
        for i in range(0, len(agent_actions)):
            new_state.state_dict["a1"][i] += agent_actions[i]
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
                terminal = True
        return terminal 
    # get to the flag, getting a winning bonus -


# generates a random initial state for the envrioment 
#state = Game((random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)),(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)),(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)))

def generate_trajectory(num_steps):
    game = Game(1, 1, 1, 1, 10)
    trajectory = []
    for i in range(num_steps):
        state = game.state_dict.copy()
        action = game.policy_random()
        #reward = game.reward(action)
        print(type(action))
        terminal = game.is_terminal()
        trajectory.append((state, action, 0, terminal))
        
        if terminal:
            break
        
        game = game.transition(action)
    
    return trajectory

temp = generate_trajectory(2)
print(temp)
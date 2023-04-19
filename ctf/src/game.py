import random 
import json 

grid_size = 10 

# records the state of the game at a given moment
class Game: # each state stores the positions, reward, action, and terminal status
    # THIS IS ONE GAME THAT HAS DIFFERENT PROPERTIES THAT CAN BE UPDATED LATER ON
    
    # def __init__(self, agent_count, obstacle_count, flag_count, action_cost, goal_reward):

    def __init__(self, action_cost, goal_reward):
        # state dictionary : agent, obstacle, flag -> coordinates 
        self.state_dict = {
            "a1": [random.randint(0, 9), random.randint(0, 9)], # agent position
            "o1": [random.randint(0, 9), random.randint(0, 9)], # obstacle position
            "f1": [random.randint(0, 9), random.randint(0, 9)]  # flag position
        }
        self.action_cost = action_cost # cost of an action (constant)
        self.goal_reward = goal_reward # reward for reaching the goal (constant)
        self.terminal = False          # if the game has ended or not
    
    # converts state dict into parsable format
    def position_map(self):    
         # format the positions of the agent, obstacle, and flag into a dictionary
        map = {}                      
        agent_position = {
            "row": self.state_dict["a1"][0],
            "col": self.state_dict["a1"][1]
        }

        obstacle_position = {
            "row": self.state_dict["o1"][0],
            "col": self.state_dict["o1"][1]
        }

        flag_position = {
            "row": self.state_dict["f1"][0],
            "col": self.state_dict["f1"][1]
        } 

        # add the positions to the map dictionary
        map["a1"] = agent_position
        map["o1"] = obstacle_position
        map["f1"] = flag_position

        return map

    # create a new state based on the current state and the chosen action
    def transition(self, action): 
        # take out the current state and take out the transition -> 
        # update the current state and directly change the game object 
        # input: currentstate, action 
        # keep track of the state that you currently having
        # obstacle detection will be in here later on - "physics part"
        
        newstate = Game(self.action_cost, self.goal_reward)
        newstate.state_dict["a1"][0] = self.state_dict["a1"][0] + action[0]
        newstate.state_dict["a1"][1] = self.state_dict["a1"][1] + action[1]
        return newstate

        '''
        for multiple agents
        
        for i in range(0, len(agent_actions)):
            state.state_dict["a1"][i] += agent_actions[i]
        '''

    # calculate the reward for taking the given action
    def reward(self, action):                                           
        if(self.state_dict["a1"] == self.state_dict["f1"]):             #if agent reaches flag, return reward for reaching goal
            return self.goal_reward
        return self.action_cost                                         # otherwise, for now return default action cost
    
    def is_terminal(self):                                              # check if the game has ended (if the agent has reached the flag)
        if(self.state_dict["a1"] == self.state_dict["f1"]):
            return True
        return False 

        '''
        for multiple agents:
        
        for agent_pos in state.state_dict["a1"]:
            if agent_pos == state.state_dict["f1"]:
                terminal = True

        '''


# choose a random move from the possible moves (up, down, left, right, stay)
def policy_random(state):
    possible_moves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)] 
    return random.choice(possible_moves)
    '''
    for multiple agents         
    agent_actions = []
    agent_actions = random.choice(possible_moves)
    return agent_actions
    '''

# Store data for multiple runthroughs of the game 
def generate_trajectory(max_episode, max_time_step):                   
    all_episode_trajectory = []                                        
    
    # Loop through the specified number of episodes
    for episode in range(max_episode):
        state = Game(-1, 10)                                           # Create a new game state object with the specified action cost and goal reward
        episode_trajectory = []                                        # Create an empty list to store the trajectory for the current episode

        # Loop through the specified number of time steps
        for i in range(max_time_step):
            ###### policy random should be a class in the future ...                                  
            action = policy_random(state)                             # Choose a random action according to a random policy
            next_state = state.transition(action)                      # Get the next state by applying the chosen action to the current state
            reward = state.reward(action)                              # Get the reward for the current state and action
            terminal = state.is_terminal()                             # Check if the current state is terminal 

            curr_state = (state.position_map(), action, reward, terminal)
            episode_trajectory.append(curr_state)

            state = next_state 
            if terminal:
                break    
        all_episode_trajectory.append(episode_trajectory)
    return all_episode_trajectory

# array that stores the result of generate_trajectory
temp = generate_trajectory(1, 3)
print(temp)

json_string = json.dumps(temp)

# converts it to json format
with open('all_episode_trajectories.json', 'w') as f:
    f.write(json_string)


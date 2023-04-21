import random 
import json 

grid_size = 10 

class Game: # each state stores the positions, reward, action, and terminal status
    # THIS IS ONE GAME THAT HAS DIFFERENT PROPERTIES THAT CAN BE UPDATED LATER ON
    

    # def __init__(self, agent_count, obstacle_count, flag_count, action_cost, goal_reward):

    def __init__(self, action_cost, goal_reward):
        # state dictionary : agent, obstacle, flag -> list of coordinates 

        self.state_dict = {
            "agent": [
                {
                    "id": "a1",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9),
                    "direction": random.choice(["up", "down", "left", "right"])
                },
                {
                    "id": "a2",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9),
                    "direction": random.choice(["up", "down", "left", "right"])
                }
            ],
            "obstacle": [
                {
                    "id": "o1",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9)
                },
                {
                    "id": "o2",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9)
                }
            ],
            "flag": [
                {
                    "id": "f1",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9)
                },
                {
                    "id": "f2",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9)
                }
            ]
        }
        self.action_cost = action_cost # cost of an action (constant)
        self.goal_reward = goal_reward # reward for reaching the goal (constant)
        self.terminal = False          # if the game has ended or not

    
    # converts state dict into parsable format
    '''
    def position_map(self):    
         # format the positions of the agent, obstacle, and flag into a dictionary
        map = {}  

        for agent in self.state_dict["agent"]:
            map[agent["id"]] =                     
        agent_position = {
            
            "row": self.state_dict["agent"][0]["pos"][0],
            "col": self.state_dict["agent"][1]["pos"][1]
        }

        obstacle_position = {
            "row": self.state_dict["obstacle"][0]["pos"][0],
            "col": self.state_dict["obstacle"][1]["pos"][1]
        }

        flag_position = {
            "row": self.state_dict["flag"][0]["pos"][0], 
            "col": self.state_dict["flag"][1]["pos"][1]
        } 

        # add the positions to the map dictionary
        map["agent"]    = agent_position
        map["obstacle"] = obstacle_position
        map["flag"]     = flag_position

        return map 
    '''
    # make the rule agents cannot run into obstacles 
    # when you have multiple agents, check multiple times 

    def transition(self, actions): 
        # take out the current state and take out the transition -> 
        # update the current state and directly change the game object 
        # input: currentstate, action 
        # keep track of the state that you currently having
        # obstacle detection will be in here later on - "physics part"
        for i in range(0, len(self.state_dict["agent"])):
            self.state_dict["agent"][i]["row"] += actions[i][0]
            self.state_dict["agent"][i]["col"] += actions[i][1]
            
        #make this not create a new state instead just update self.state_dict directly
        # dont return anything
        

        '''
        for i in range(0, len(agent_actions)):
            state.state_dict["a1"][i] += agent_actions[i]
        '''

    # calculate the reward for taking the given action
    def reward(self, actions): 
        rewards = [0 for i in range(len(actions))]
        for i in range(len(actions)):
            agent = self.state_dict["agent"][i]
            row = agent["row"]
            col = agent["col"]
            for flag in self.state_dict["flag"]:
                if row == flag["row"] and col == flag["col"]:
                    rewards[i] += self.goal_reward
                else:
                    rewards[i] += self.action_cost
        
        return rewards
                                                # otherwise, for now return default action cost
    
    def is_terminal(self):                                              # check if the game has ended (if the agent has reached the flag)
        for agent in self.state_dict["agent"]:
            row = agent["row"]
            col = agent["col"]
            for flag in self.state_dict["flag"]:
                if row == flag["row"] and col == flag["col"]:
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
    agent_actions = []
    possible_moves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)] 

    for agent in state.state_dict["agent"]:
        agent_actions.append(random.choice(possible_moves))
    
    return agent_actions
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
            actions = policy_random(state)                             # Choose a random action according to a random policy
            reward = state.reward(actions)                              # Get the reward for the current state and action
            terminal = state.is_terminal()                             # Check if the current state is terminal 
            curr_state = (state.state_dict, actions, reward, terminal)
            state.transition(actions)                      # Get the next state by applying the chosen action to the current state

            episode_trajectory.append(curr_state)

            if terminal:
                break    
        all_episode_trajectory.append(episode_trajectory)
    return all_episode_trajectory

# array that stores the result of generate_trajectory
temp = generate_trajectory(1, 1)
print(temp)

json_string = json.dumps(temp)

# converts it to json format
with open('all_episode_trajectories.json', 'w') as f:
    f.write(json_string)


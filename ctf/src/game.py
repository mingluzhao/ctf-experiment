import random 
import json 


class Game: # each state stores the positions, reward, action, and terminal status
    # THIS IS ONE GAME THAT HAS DIFFERENT PROPERTIES THAT CAN BE UPDATED LATER ON
    grid_size = 10 

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


     # take out the current state and take out the transition -> 
        # update the current state and directly change the game object 
        # keep track of the state that you currently having
        # obstacle detection will be in here later on - "physics part"

    def transition(self, actions): 
        for i in range(0, len(self.state_dict["agent"])):
            prev_row = self.state_dict["agent"][i]["row"]
            prev_col = self.state_dict["agent"][i]["col"]
            self.state_dict["agent"][i]["row"] += actions[i][0]
            self.state_dict["agent"][i]["col"] += actions[i][1]
            curr_row = self.state_dict["agent"][i]["row"]
            curr_col = self.state_dict["agent"][i]["col"]
            if curr_row < 0 or curr_row >= self.grid_size or curr_col < 0 or curr_col >= self.grid_size:
            # undo the invalid move by reverting to the previous position
                self.state_dict["agent"][i]["row"] = prev_row
                self.state_dict["agent"][i]["col"] = prev_col


            #self.state_dict["agent"][i]["row"] += actions[i][0]
            #self.state_dict["agent"][i]["col"] += actions[i][1]
            
        # edge detection 
        # consider if the agents are bumping into each other / edge detection 


        # make this not create a new state instead just update self.state_dict directly
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
        state = Game(-1, 10)                                          
        episode_trajectory = []                                        

        # Loop through the specified number of time steps
        for i in range(max_time_step):
            ###### policy random should be a class in the future ...                                  
            actions = policy_random(state)                            
            reward = state.reward(actions)                            
            terminal = state.is_terminal()                           
            curr_state = (state.state_dict, actions, reward, terminal)
            state.transition(actions)                                

            episode_trajectory.append(curr_state)

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


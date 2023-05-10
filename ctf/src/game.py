import random 
import json 

grid_size = 10 
movement_coords = [[0,1], [1,0], [0,-1], [-1,0]]

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

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
                    "direction": random.choice(0,3)
                },
                {
                    "id": "a2",
                    "row": random.randint(0, 9),
                    "col": random.randint(0, 9),
                    "direction": random.choice(0,3)
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
        blocked = False
        for agent, action in zip(self.state_dict["agent"], actions):
            curr_row = agent["row"]
            curr_row = agent["col"]
            new_row = curr_row
            new_row = curr_row
            if action == "forward":
                move = movement_coords[agent["direction"]]
                new_row =  curr_row + move[0]
                new_col =  curr_row + move[1]
            elif action == "backward":
                move = movement_coords[agent["direction"]]
                new_row =  curr_row + move[0]
                new_col =  curr_row + move[1]
            elif action == "turn_r":
                if agent["direction"] == 4:
                    agent["direction"] = 0
                else:
                    agent["direction"] += 1
            elif action == "turn_l":
                if agent["direction"] == 0:
                    agent["direction"] = 4
                else:
                    agent["direction"] -= 1
    
            # check if agent is moving into obstacle
            for obstacle in self.state_dict["obstacle"]:
                if new_row == obstacle["row"] and new_col == obstacle["col"]:
                    blocked = True
            # check if agent is moving into another agent
            for other_agent in self.state_dict["agent"]:
                if agent is other_agent:
                    pass
                elif new_row == other_agent["row"] and new_col == other_agent["col"]:
                    blocked = True
            # check if agent is moving out of grid
            if new_row < 0 or new_row >= self.grid_size or new_col < 0 or new_col >= self.grid_size:
                blocked = True
            # undo the invalid move by reverting to the previous position
            if blocked == False:
                agent["row"] = new_row
                agent["col"] = new_col
            blocked = False
            
        # edge detection 
        # consider if the agents are bumping into each other / edge detection 


        # make this not create a new state instead just update self.state_dict directly
        # dont return anything


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

# choose a random move from the possible moves (up, down, left, right, stay)
def policy_random(state):
    agent_actions = []
    possible_moves = ["forward", "backward", "turn_r", "turn_l"] 

    for agent in state.state_dict["agent"]:
        agent_actions.append(random.choice(possible_moves))
    
    return agent_actions

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


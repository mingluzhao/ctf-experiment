import random 
import json 

grid_size = 10

class Game: # each state stores the positions, reward, action, and terminal status
    
    # def __init__(self, agent_count, obstacle_count, flag_count, action_cost, goal_reward):

    def __init__(self, action_cost, goal_reward):
        self.state_dict = {
            "a1": [random.randint(0, 9), random.randint(0, 9)],
            "o1": [random.randint(0, 9), random.randint(0, 9)],
            "f1": [random.randint(0, 9), random.randint(0, 9)]
        }
        self.action_cost = action_cost 
        self.goal_reward = goal_reward
        self.terminal = False
        
    def position_map(self):
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

        map["a1"] = agent_position
        map["o1"] = obstacle_position
        map["f1"] = flag_position

        return map

    def policy_random(self): 
        possible_moves = [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)] 
        return random.choice(possible_moves)

        '''
        for multiple agents 
        
        agent_actions = []
        agent_actions = random.choice(possible_moves)
        return agent_actions
        '''
    
    def transition(self, action):
        newstate = Game(self.action_cost, self.goal_reward)
        newstate.state_dict["a1"][0] = self.state_dict["a1"][0] + action[0]
        newstate.state_dict["a1"][1] = self.state_dict["a1"][1] + action[1]
        return newstate

        '''
        for multiple agents
        
        for i in range(0, len(agent_actions)):
            state.state_dict["a1"][i] += agent_actions[i]
        '''
    
    def reward(self, action):
        if(self.state_dict["a1"] == self.state_dict["f1"]): #if agent reaches flag, return reward for reaching goal
            return self.goal_reward
        return self.action_cost #otherwise, for now return default action cost
    
    def is_terminal(self): 
        if(self.state_dict["a1"] == self.state_dict["f1"]):
            return True
        return False 

        '''
        for multiple agents:
        
        for agent_pos in state.state_dict["a1"]:
            if agent_pos == state.state_dict["f1"]:
                terminal = True
        '''
        
def generate_trajectorys(max_episode, max_time_step):
    all_episode_trajectory = []
    for episode in range(max_episode):
        state = Game(-1, 10)  
        episode_trajectory = []
        for i in range(max_time_step):
            action = state.policy_random()
            next_state = state.transition(action)
            reward = state.reward(action)
            terminal = state.is_terminal()

            curr_state = (state.position_map(), action, reward, terminal)
            episode_trajectory.append(curr_state)

            state = next_state
            if terminal:
                break    
        all_episode_trajectory.append(episode_trajectory)
    return all_episode_trajectory

temp = generate_trajectorys(1, 3)
print(temp)

json_string = json.dumps(temp)

with open('all_episode_trajectories.json', 'w') as f:
    f.write(json_string)


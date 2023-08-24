import random 
import json 
from constants import *
import copy
        
class Game:     
    #reset: reset the state to a optionally specified state

    def __init__(self, action_cost, goal_reward, init_dict, max_steps, max_round, full_visible):
        # state dictionary : agent, obstacle, flag -> list of coordinates 
        self.init_dict = copy.deepcopy(init_dict)
        self.state_dict = copy.deepcopy(init_dict)
        self.action_cost = action_cost # cost of an action (constant)
        self.goal_reward = goal_reward # reward for reaching the goal (constant)

        self.max_steps = max_steps
        self.max_round = max_round
        self.steps = 0
        self.round = 1

        self.fill_visible = full_visible

        self.grid = [['_' for _ in range(grid_size)] for _ in range(grid_size)]
        
        for item_type in init_dict:
            for item in init_dict[item_type]:
                if item_type == 'agent':
                    self.grid[item['row']][item['col']] = 'a' + item['color'][0]
                elif item_type == 'flag':
                    self.grid[item['row']][item['col']] = 'f' + item['color'][0]
                elif item_type == 'obstacle':
                    self.grid[item['row']][item['col']] = 'o'
    
    def update_grid(self):
        self.grid = [['_' for _ in range(10)] for _ in range(10)]
        for item_type in self.state_dict:
            for item in self.state_dict[item_type]:
                if item_type == 'agent':
                    self.grid[item['row']][item['col']] = 'a' + item['color'][0]
                elif item_type == 'flag':
                    self.grid[item['row']][item['col']] = 'f' + item['color'][0]
                elif item_type == 'obstacle':
                    self.grid[item['row']][item['col']] = 'o'
    
    def observe(self, agent):
        view = [['x' for _ in range(3)] for _ in range(3)]
        direction = agent['direction']
        row, col = agent['row'], agent['col']

        # Calculate the offsets based on the direction the agent is facing
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
        dx, dy = offsets[direction]

        # Start from the square in front of the agent
        for i in range(3):
            for j in range(3):
                x = row + dx*(i-1)
                y = col + dy*(j-1)
                
                # Check if coordinates are inside the grid
                if 0 <= x < 10 and 0 <= y < 10:
                    view[i][j] = self.grid[x][y]
                    
        return view

    def find_by_position(self, row, col):
        for items in self.state_dict.values():
            for item in items:
                if item['row'] == row and item['col'] == col:
                    return item
        return None

    def move(self, agent, row, col):
        if row < 0 or row > 9 or col < 0 or col > 9:  # Agent cannot move outside the grid
            return False
        occupied = self.find_by_position(row, col)
        if occupied:
            if occupied['id'] == agent['id']:  # if agent moved to the same spot
                return False
            elif 'direction' in occupied:  # if spot is occupied by another agent
                return False
            elif occupied['id'][0] == 'f': # if spot occupied by flag, continue
                pass
            else:  # if spot is occupied by an obstacle
                return False
        agent['row'] = row
        agent['col'] = col
        return True
    
    def transition(self, actions):
        new_positions = []
        for action, agent in zip(actions, self.state_dict['agent']):
            new_row, new_col = agent['row'], agent['col']
            if action == 'forward':
                new_row, new_col = self.calculate_forward_position(agent)
            elif action == 'backward':
                new_row, new_col = self.calculate_backward_position(agent)
            elif action == 'left':
                agent['direction'] = (agent['direction'] - 1) % 4
                continue
            elif action == 'right':
                agent['direction'] = (agent['direction'] + 1) % 4
                continue
            new_positions.append((agent, new_row, new_col))
        
        random.shuffle(new_positions)
        for agent, new_row, new_col in new_positions:
            self.move(agent, new_row, new_col)
        
        self.update_grid()
        self.steps += 1
    
    def calculate_forward_position(self, agent):
        direction = agent['direction']
        row, col = agent['row'], agent['col']
        if direction == 0:  # Up
            return row - 1, col
        elif direction == 1:  # Right
            return row, col + 1
        elif direction == 2:  # Down
            return row + 1, col
        elif direction == 3:  # Left
            return row, col - 1
            
    def calculate_backward_position(self, agent):
        direction = agent['direction']
        row, col = agent['row'], agent['col']
        if direction == 0:  # Up
            return row + 1, col
        elif direction == 1:  # Right
            return row, col - 1
        elif direction == 2:  # Down
            return row - 1, col
        elif direction == 3:  # Left
            return row, col + 1
        
    # calculate the reward for taking the given action
    def reward(self):
        rewards = []
        for agent in self.state_dict['agent']:
            agent_reward = self.action_cost
            for flag in self.state_dict['flag']:
                if agent['row'] == flag['row'] and agent['col'] == flag['col'] and agent['color'] != flag['color']:
                    agent_reward = self.goal_reward
            rewards.append(agent_reward)
        return rewards
                                                # otherwise, for now return default action cost
    
    def is_terminal(self):
        if self.steps == self.max_steps:
            return True
        for agent in self.state_dict['agent']:
            for flag in self.state_dict['flag']:
                if agent['row'] == flag['row'] and agent['col'] == flag['col'] and agent['color'] != flag['color']:
                    return True
        return False
    
    def is_final_terminal(self):
        if self.round > self.max_round:
            return True
        return False
    
    def is_full_visible(self):
        return self.fill_visible
    
    def reset(self):
        self.round += 1
        self.steps = 0
        self.state_dict = copy.deepcopy(self.init_dict)
    
# choose a random move from the possible moves (up, down, left, right, stay)
def policy_random(state):
    actions = []
    for agent in state["agent"]:
        actions.append(random.randint(0,3))
    return actions

def run(num_episodes, max_steps):
    # Initialize environment and agent
    game = Game(-1, 10, init_state)
    trajectory_list = []

    # Loop over episodes
    for i_episode in range(num_episodes):
        eps_traj = []
        # Reset the state of the environment
        game.reset()
        state = game.state_dict
        # Loop over steps within this episode
        for t in range(max_steps):
            # The agent selects an action
            moves = policy_random(game.state_dict)
            str_moves = [possible_moves[x] for x in moves]

            # Execute the action and get feedback
            next_state = game.transition(str_moves)
            reward = game.reward(str_moves)
            is_terminal = game.is_terminal()
            # Append information to trajectory

            # Keep track of trajectory
            # state, obv, moves, reward, next_state, is_terminal
            # obv is array of observations
            eps_traj.append([state, moves, reward, next_state, is_terminal])

            # Update the current state
            state = next_state

            # End this episode if done
            if is_terminal:
                break

        trajectory_list.append(eps_traj)
    
    json_string = json.dumps(game.state_dict)
    with open('./run_trajectory.json', 'w') as f:
        f.write(json_string)


def main():
    traj_list = run(1, 5)
    print(traj_list)

if __name__ == '__main__':
    main()
import random 
import os
import json 
from constants import *
import copy
from datetime import datetime

        
class Game:     
    #reset: reset the state to a optionally specified state

    def __init__(self, action_cost, goal_reward, init_dict, max_steps, max_round, full_visible, save_toggle, obstacle_maps):
        # state dictionary : agent, obstacle, flag -> list of coordinates 
        self.obstacle_maps = obstacle_maps
        self.obstacle_counter = 0

        if not obstacle_maps:
            init_dict['obstacle'] = self.generate_obstacles(num_obstacles)
        else:
            init_dict['obstacle'] = self.obstacle_maps[self.obstacle_counter]

        self.init_dict = copy.deepcopy(init_dict)
        self.state_dict = copy.deepcopy(init_dict)
        self.action_cost = action_cost # cost of an action (constant)
        self.goal_reward = goal_reward # reward for reaching the goal (constant)
        
        self.full_visible = full_visible
        self.save_toggle = save_toggle

        self.max_steps = max_steps
        self.max_round = max_round
        self.steps = 0
        self.round = 1

        self.agent_trajectories = [{0: [], 1: [], 2: [], 3: []}] * self.max_round

        self.update_arena()
    
    def update_arena(self):
        self.grid = [[['e'] for _ in range(10)] for _ in range(10)]
        for item in self.state_dict['obstacle']:
            self.grid[item['row']][item['col']] = ['o']
        for item in self.state_dict['flag_base']:
            self.grid[item['row']][item['col']] = ['b', item]
        self.grid = self.padGrid()
        
    def padGrid(self):
        # Get the dimensions of the input grid
        rows = len(self.grid)
        cols = len(self.grid[0]) if rows > 0 else 0
        
        # Initialize a new 2D array with dimensions (rows+2) x (cols+2)
        # Fill it with 'x' initially
        padded_grid = [[['x'] for _ in range(cols + 2)] for _ in range(rows + 2)]
        
        # Copy the original grid into the new grid, starting from index (1,1)
        for i in range(rows):
            for j in range(cols):
                padded_grid[i + 1][j + 1] = self.grid[i][j]
                
        return padded_grid
    
    def grid_state(self):
        full_arena = copy.deepcopy(self.grid)
        for agent in self.state_dict['agent']:
            r, c = agent['row'], agent['col']
            full_arena[r + 1][c + 1] = ['a', agent]
        
        return full_arena
    
    def observe(self, agent):
        view = [[['x'] for _ in range(3)] for _ in range(3)]
        direction = agent['direction']
        row, col = agent['row'], agent['col']

        # Calculate the offsets based on the direction the agent is facing
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up, Right, Down, Left
        dx, dy = offsets[direction]

        grid = self.grid_state()
        print(grid)
        # Start from the square in front of the agent
        for i in range(3):
            for j in range(3):
                x = row + dx*(i-1)
                y = col + dy*(j-1)
                
                # Check if coordinates are inside the grid
                if 0 <= x < 10 and 0 <= y < 10:
                    view[i][j] = grid[x][y]
                    
        return view

    def generate_obstacles(self, num):
        agent_coords = [(0, 0), (0, 9), (9,0), (9,9)]
        obstacle_coords = []
        obstacles = []

        for i in range(num):
            coord = (random.randint(0, 9),  random.randint(0, 9))
            while coord in agent_coords or coord in obstacle_coords:
                coord = (random.randint(0, 9),  random.randint(0, 9))
            obstacle_coords.append(coord)

            obstacles.append({'id': 'o' + str(i), 'row': coord[0], 'col': coord[1]})
        
        return obstacles
            
    def find_by_position(self, row, col):
        objects = []
        for type, items in self.state_dict.items():
            for item in items:
                if item['row'] == row and item['col'] == col:
                    objects.append((type, item))
        return objects

    def move(self, agent, row, col):
        if row < 0 or row > 9 or col < 0 or col > 9:  # Agent cannot move outside the grid
            return False
        objects = self.find_by_position(row, col)
        for type, obj in objects:
            if type == 'obstacle': # if spot occupied by obstacle, return False
                return False
            else:  # if spot has agent or flag
                pass
        agent['row'] = row
        agent['col'] = col
        return True
        
    def transition(self, actions):
        original_state = copy.deepcopy(self.state_dict)
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
        
        self.check_flags()
        self.update_arena()
        self.steps += 1

        rewards = self.reward()
        for i in range(0, 4):
            agent = self.state_dict["agent"][i]
            action = move_map.get(actions[i], -1)
            reward = rewards[i]
            self.agent_trajectories[self.round - 1][i].append([self.state_dict, self.observe(agent), action, reward, original_state, self.is_terminal()])
    
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
            for flag in self.state_dict['flag_base']:
                if agent['row'] == flag['row'] and agent['col'] == flag['col'] and agent['color'] != flag['color']:
                    agent_reward = self.goal_reward
            rewards.append(agent_reward)
        return rewards
                                                # otherwise, for now return default action cost
    
    def check_flags(self):
        agents, bases = self.state_dict['agent'], self.state_dict['flag_base']

        for agent in agents:
            for base in bases:
                if agent['row'] == base['row'] and agent['col'] == base['col'] and agent['color'] != base['color'] and base['hasflag']:
                    agent['flagStatus'] = base['color']
                    base['hasflag'] = False

        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                agent1 = agents[i]
                agent2 = agents[j]

                if agent1['row'] == agent2['row'] and agent1['col'] == agent2['col']:
                    if agent1['color'] != agent2['color']:
                        if agent1['flagStatus'] and not agent2['flagStatus']:
                            agent2['flagStatus'] = agent1['flagStatus']
                            agent1['flagStatus'] = None
                        elif agent2['flagStatus'] and not agent1['flagStatus']:
                            agent1['flagStatus'] = agent2['flagStatus']
                            agent2['flagStatus'] = None

    def is_terminal(self):
        if self.steps == self.max_steps:
            return True
        return False
    
    def is_final_terminal(self):
        if self.round >= self.max_round:
            return True
        return False
    
    def is_full_visible(self):
        return self.full_visible
    
    def save_on(self):
        return self.save_toggle
        
    def reset(self):
        self.round += 1
        self.steps = 0
        if self.obstacle_maps:
            self.obstacle_counter = (self.obstacle_counter + 1) % len(self.obstacle_maps)
            self.init_dict['obstacle'] = self.obstacle_maps[self.obstacle_counter]
        else:
            self.init_dict['obstacle'] = self.generate_obstacles(num_obstacles)
        self.state_dict = copy.deepcopy(self.init_dict)
    
    def save(self, roomID):
        data_directory_path = os.path.join('..', 'data')

        if not os.path.exists(data_directory_path):
            os.makedirs(data_directory_path)

        now = datetime.now()
        date_prefix = str(now.year) + '_' + str(now.month).zfill(2) + str(now.day).zfill(2)
        hour_str = str(now.hour).zfill(2)
        minute_str = str(now.minute).zfill(2)
        time_prefix = hour_str + minute_str

        trajectories =[[] for _ in range(4)]

        for round_data in self.agent_trajectories:
            for id in round_data:
                trajectories[id].append(round_data[id])
        
        for id in range(0, 4):
            file_name = date_prefix + '_' + time_prefix + '_' + str(roomID) + '_0' + str(id) + '.json'
            file_path = os.path.join(data_directory_path, file_name)
            with open(file_path, "w") as outfile:
                json.dump(trajectories[id], outfile)
        
    
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
    game = Game(-1, 10, init_state, max_steps, max_round, full_visible, save_toggle, obstacle_maps)
    print(game.observe(game.state_dict['agent'][1]))

if __name__ == '__main__':
    main()
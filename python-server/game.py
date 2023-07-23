import random 
import json 
from constants import *
import copy
        
class Game:     
    #reset: reset the state to a optionally specified state

    def __init__(self, action_cost, goal_reward, init_dict):
        # state dictionary : agent, obstacle, flag -> list of coordinates 
        self.init_dict = copy.deepcopy(init_dict)
        self.state_dict = copy.deepcopy(init_dict)
        self.action_cost = action_cost # cost of an action (constant)
        self.goal_reward = goal_reward # reward for reaching the goal (constant)
        self.terminal = False          # if the game has ended or not
        self.agent_count = 0

    #add new agents to the game
    def add_agent(self, client_id):
        self.agent_count += 1
        new_agent = {
            "id": f"a{self.agent_count}",
            "row": random.randint(0, 9),
            "col": random.randint(0, 9),
            "direction": random.randint(0,3)
        }
        self.state_dict["agent"].append(new_agent)

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
            else:  # if spot is occupied by an obstacle or flag
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
            for flag in self.state_dict['flags']:
                if agent['row'] == flag['row'] and agent['col'] == flag['col'] and agent['color'] != flag['color']:
                    agent_reward = self.goal_reward
            rewards.append(agent_reward)
        return rewards
                                                # otherwise, for now return default action cost
    
    def is_terminal(self):
        for agent in self.state_dict['agent']:
            for flag in self.state_dict['flags']:
                if agent['row'] == flag['row'] and agent['col'] == flag['col'] and agent['color'] != flag['color']:
                    return True
        return False
    
    def reset(self):
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
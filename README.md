GENERAL GAME RULES
- partial observability: each agent can only see the 3x3 grids in front of it
- movement: TURN_LEFT [A], TURN_RIGHT[D], MOVE[W]

  
CURRENT PROGRESS:
- game is played with 4 agents, two on the red team, two on the blue team.
- there are three modes in which the game can be played:
    - random: all 4 agents are randomly controlled.
    - two player: one team of agents is controlled by human keyboard input
    - four player: all agents are controlled by a human client
- all agents move in fixed 0.5 intervals: in other words, they all transition together. It follows that for human controlled agents, only the first keypress is reigstered in each 0.5 second interval.
- agents cannot move on top of eachother, but may swap places. Additionally, they cannot move through obstacles or the game border. 
- currently, a player wins if they reach the flag on the other side of the arena
- the server can support multiple concurrent games of different modes by utilizing rooms.

STEPS TO RUN THE GAME: 
1. log into a lab computer, using Dr. Gao's ssh login and password
    - 'ssh taogao@[LAB_IP_ADDRESS]'
    - pwd: [PASSWORD]
2. activate the existing conda environment 'ctf_env' using 'conda activate ctf_env'
3. find the ctf-experiment directory:
    - in the server directory, run 'python server.py' to start the server.
    - in the ctf directoy, run 'npm start' to compile the game and start the first client
4. any subsequent clients can be opened on any device using the url '[LAB_IP_ADRESS]:3000' 

OVERVIEW OF PROJECT FILES:

python-server is the directory containing the game logic and backend server. 

- game.py contains all of the core game mechanics. It tracks the state of all objects in the game, and transitions them when necessary.

- server.py is the backend server for this game. It handles client connection and disconnection, and organizes all the clients into rooms. It manages one game per room. It handles keyboard input, translating that into agent movement. 

- constants.py contain some presets for the game, including the initial state.

ctf is the directory containing the react app serving as the game's frontend.

- App.js is our main file. It contains all of the screen components, from the start screen to the waiting screen to the main display. It will render these screens depending on the configurations/state of the game, which it recieves through button presses and dropdown selections. It will also detect keypresses during gameplay to relay to the server. It returns a component that will render the game arena along with the agents within it.

To help render the game, App makes use of a few additional components.

- SquareParent.js returns a component that represents a square on our game grid. It can be rendered as an empty, obstacle, border, or flag square.

- GameBoard.js will return an array of SquareParent components, and render them in a grid.



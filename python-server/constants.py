grid_size = 10 

possible_moves = ["forward", "backward", "turn_r", "turn_l"] 
move_map = {'forward': 0, 'right': 1, 'backward': 2, 'left': 3}

# ADJUSTABLE PARAMETERS
save_toggle = False
max_steps = 200
max_round = 1
full_visible = True
num_obstacles = 8
step_time = 0.5

init_state = {
            "agent": [
                {
                    "id": 0,
                    "row": 0,
                    "col": 0,
                    "color": "red",
                    "direction": 1,
                    "flagStatus": None
                },
                {
                    "id": 1,
                    "row": 0,
                    "col": 9,
                    "color": "red",
                    "direction": 3,
                    "flagStatus": None
                },
                {
                    "id": 2,
                    "row": 9,
                    "col": 0,
                    "color": "blue",
                    "direction": 1,
                    "flagStatus": None
                },
                {
                    "id": 3,
                    "row": 9,
                    "col": 9,
                    "color": "blue",
                    "direction": 3,
                    "flagStatus": None
                }
            ],
            "obstacle": [],
            "flag_base": [
                {
                    "id": "f1",
                    "color": "red",
                    "row": 0,
                    "col": 5,
                    "hasflag": True
                },
                {
                    "id": "f2",
                    "color": "blue",
                    "row": 9,
                    "col": 5,
                    "hasflag": True
                },
            ]
        }

obstacle_maps = [[{
                    "id": "o1",
                    "row": 0,
                    "col": 1
                },
                {
                    "id": "o2",
                    "row": 1,
                    "col": 1
                },
                {
                    "id": "o3",
                    "row": 2,
                    "col": 1
                },
                {
                    "id": "o4",
                    "row": 7,
                    "col": 7
                }],
                [{
                    "id": "o1",
                    "row": 3,
                    "col": 3
                },
                {
                    "id": "o2",
                    "row": 2,
                    "col": 7
                },
                {
                    "id": "o3",
                    "row": 7,
                    "col": 2
                },
                {
                    "id": "o4",
                    "row": 7,
                    "col": 7
                }],
                [{
                    "id": "o1",
                    "row": 2,
                    "col": 2
                },
                {
                    "id": "o2",
                    "row": 3,
                    "col": 6
                },
                {
                    "id": "o3",
                    "row": 7,
                    "col": 2
                },
                {
                    "id": "o4",
                    "row": 7,
                    "col": 7
                }]]
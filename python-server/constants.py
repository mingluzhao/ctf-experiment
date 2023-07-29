grid_size = 10 
possible_moves = ["forward", "backward", "turn_r", "turn_l"] 

init_state = {
            "agent": [
                {
                    "id": 0,
                    "row": 0,
                    "col": 0,
                    "color": "red",
                    "direction": 1
                },
                {
                    "id": 1,
                    "row": 0,
                    "col": 9,
                    "color": "red",
                    "direction": 3
                },
                {
                    "id": 2,
                    "row": 9,
                    "col": 0,
                    "color": "blue",
                    "direction": 1
                },
                {
                    "id": 3,
                    "row": 9,
                    "col": 9,
                    "color": "blue",
                    "direction": 3
                }
            ],
            "obstacle": [
                {
                    "id": "o1",
                    "row": 2,
                    "col": 2
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
                }
            ],
            "flag": [
                {
                    "id": "f1",
                    "color": "red",
                    "row": 0,
                    "col": 5
                },
                {
                    "id": "f2",
                    "color": "blue",
                    "row": 9,
                    "col": 5
                },
            ]
        }


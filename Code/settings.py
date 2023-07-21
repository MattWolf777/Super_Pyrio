# This file contains fundamental data about the game and information related to enemy sprites.

# Number of vertical tiles in the game.
vertical_tile_number = 14

# Size of each tile in pixels.
tile_size = 64

# Height and width of the game screen in pixels.
screen_height = 900
screen_width = 1600

# Size of the player's sprite (width, height).
player_size = (42, 60)

# List of tuples representing enemy sprites' data.
# Each tuple contains information like the starting frame index, vertical position, width, height, frame count, and name of the enemy sprite.
enemy_tile_list = [
    (0, 0, 64, 64, 3, "goomba"),
    (3, 64, 64, 64, 3, "dark-goomba"),
    (6, 128, 64, 107, 3, "turtle"),
    (9, 235, 64, 107, 3, "red-turtle"),
]

# Dictionary containing specifications for different enemy sprites.
# Each enemy is identified by its name, and the corresponding dictionary contains attributes like the starting frame index, vertical position, width, height, and frame count.
enemy_specifications = {
    "goomba": {
        "start_frame_index": 0,
        "vertical_position": 0,
        "width": 64,
        "height": 64,
        "frame_count": 3,
    },
    "dark-goomba": {
        "start_frame_index": 3,
        "vertical_position": 64,
        "width": 64,
        "height": 64,
        "frame_count": 3,
    },
    "turtle": {
        "start_frame_index": 6,
        "vertical_position": 128,
        "width": 64,
        "height": 107,
        "frame_count": 3,
    },
    "red-turtle": {
        "start_frame_index": 9,
        "vertical_position": 235,
        "width": 64,
        "height": 107,
        "frame_count": 3,
    },
}

# Dictionary mapping enemy IDs to their corresponding enemy specifications.
# Each enemy is identified by a unique ID (e.g., "0", "1", "2", "3") associated with the enemy name and specifications.
enemies_by_id = {
    "0": enemy_specifications["goomba"],
    "1": enemy_specifications["dark-goomba"],
    "2": enemy_specifications["turtle"],
    "3": enemy_specifications["red-turtle"],
}

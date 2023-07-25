"""
This file contains data about the ../Levels, such as:
    - The CSV files, containing the data_map of the level
    - The node position describing the location on the overworld map
    - The next level, to be unlocked
    - The background color of the level
"""
level_1 = {
    "base": "../Levels/1/Level_1_base.csv",
    "animated": "../Levels/1/Level_1_animated.csv",
    "background": "../Levels/1/Level_1_background.csv",
    "constrains": "../Levels/1/Level_1_constrains.csv",
    "enemies": "../Levels/1/Level_1_mobs.csv",
    "player": "../Levels/1/Level_1_player.csv",
    "goal": "../Levels/1/Level_1_goal.csv",
    "node_pos": (475, 530),
    "unlock": 2,
    "background_color": (0, 171, 240),
}

level_2 = {
    "base": "../Levels/2/Level_2_base.csv",
    "animated": "../Levels/2/Level_2_animated.csv",
    "background": "../Levels/2/Level_2_background.csv",
    "constrains": "../Levels/2/Level_2_constrains.csv",
    "enemies": "../Levels/2/Level_2_mobs.csv",
    "player": "../Levels/2/Level_2_player.csv",
    "goal": "../Levels/2/Level_2_goal.csv",
    "node_pos": (660, 530),
    "unlock": 3,
    "background_color": (0, 0, 0),
}

level_3 = {
    "base": "../Levels/3/Level_3_base.csv",
    "animated": "../Levels/3/Level_3_animated.csv",
    "background": "../Levels/3/Level_3_background.csv",
    "constrains": "../Levels/3/Level_3_constrains.csv",
    "enemies": "../Levels/3/Level_3_mobs.csv",
    "player": "../Levels/3/Level_3_player.csv",
    "goal": "../Levels/3/Level_3_goal.csv",
    "node_pos": (660, 340),
    "unlock": 4,
    "background_color": (0, 171, 240),
}

level_4 = {
    "base": "../Levels/4/Level_4_base.csv",
    "animated": "../Levels/4/Level_4_animated.csv",
    "background": "../Levels/4/Level_4_background.csv",
    "constrains": "../Levels/4/Level_4_constrains.csv",
    "enemies": "../Levels/4/Level_4_mobs.csv",
    "player": "../Levels/4/Level_4_player.csv",
    "goal": "../Levels/4/Level_4_goal.csv",
    "node_pos": (660, 205),
    "background_color": (0, 0, 0),
    "unlock": 5,
}
level_5 = {
    "base": "../Levels/4/Level_4_base.csv",
    "animated": "../Levels/4/Level_4_animated.csv",
    "background": "../Levels/4/Level_4_background.csv",
    "constrains": "../Levels/4/Level_4_constrains.csv",
    "enemies": "../Levels/4/Level_4_mobs.csv",
    "player": "../Levels/4/Level_4_player.csv",
    "goal": "../Levels/4/Level_4_goal.csv",
    "node_pos": (890, 205),
    "unlock": 5,
}

levels = {1: level_1, 2: level_2, 3: level_3, 4: level_4, 5: level_5}

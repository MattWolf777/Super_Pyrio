import pygame
from csv import reader
from settings import tile_size, enemy_tile_list
import os


def import_states(path):
    """
    Imports a collection of character states (animations) from the specified path.

    Parameters:
        path (str): The path to the root folder containing character state animations.

    Returns:
        states (dict): A dictionary containing character states, organized by form and movement.
    """
    states = {}
    root_folder = path

    for forms in os.listdir(root_folder):
        full_path = root_folder + forms + "/"
        states[forms] = {}
        for moves in os.listdir(full_path):
            full_path = root_folder + forms + "/" + moves + "/"
            states[forms][moves] = []
            for _, __, img_files in os.walk(full_path):
                for img in img_files:
                    full_path = root_folder + forms + "/" + moves + "/" + img
                    image_surface = pygame.image.load(full_path)
                    states[forms][moves].append(image_surface)

    return states


def import_folder(path):
    """
    Imports a collection of image frames from the specified path.

    Parameters:
        path (str): The path to the folder containing image frames.

    Returns:
        frames (list): A list of pygame.Surface objects representing the image frames.
    """
    frames = []

    for img_files in os.listdir(path):
        full_path = path + "/" + img_files
        image_surface = pygame.image.load(full_path)
        frames.append(image_surface)

    return frames


def import_csv_layout(path):
    """
    Imports a terrain map layout from a CSV file.

    Parameters:
        path (str): The path to the CSV file containing the terrain map layout.

    Returns:
        terrarin_map (list): A list representing the terrain map layout.
    """
    terrarin_map = []
    with open(path) as map:
        level = reader(map, delimiter=",")
        for row in level:
            terrarin_map.append(list(row))

        return terrarin_map


def import_cut_graphics(path, type, pos=(0, 0)):
    """
    Imports and cuts graphics from the specified path.

    Parameters:
        path (str): The path to the image file.
        type (str): The type of graphics to import ("coin" or "enemy").
        pos (tuple, optional): The position to start cutting the graphics. Defaults to (0, 0).

    Returns:
        cut_tiles (list): A list of pygame.Surface objects representing the cut graphics.
    """
    surface = pygame.image.load(path).convert_alpha()

    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    if type != "enemy":
        if type == "coin":
            coin_surf = pygame.Surface((tile_size, tile_size))
            coin_surf.blit(
                surface,
                (0, 0),
                pygame.Rect(pos[0], pos[1], tile_size, tile_size),
            )
            return coin_surf

        for row in range(tile_num_y):
            for col in range(tile_num_x):
                x = col * tile_size
                y = row * tile_size
                new_surf = pygame.Surface((tile_size, tile_size))
                new_surf.blit(
                    surface,
                    (0, 0),
                    pygame.Rect(x, y, tile_size, tile_size),
                )
                new_surf.set_colorkey((0, 0, 0))
                cut_tiles.append(new_surf)

    else:
        for enemy in enemy_tile_list:

            tile_width = enemy[2]
            tile_height = enemy[3]

            for col in range(enemy[4]):
                x = col * tile_width
                y = enemy[1]
                new_surf = pygame.Surface((tile_width, tile_height))
                new_surf.blit(
                    surface, (0, 0), pygame.Rect(x, y, tile_width, tile_height)
                )
                new_surf.set_colorkey((0, 0, 0))
                cut_tiles.append(new_surf)

    return cut_tiles

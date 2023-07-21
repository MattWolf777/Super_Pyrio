import pygame
from csv import reader
import os


def import_folder(path):
    frames = []

    for img_files in os.listdir(path):
        full_path = path + "/" + img_files
        image_surface = pygame.image.load(full_path)
        frames.append(image_surface)

    return frames

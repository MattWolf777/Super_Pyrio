import pygame, sys
from settings import *
from overworld import Overworld
from support import *
from level_intro import Level


class Game:
    def __init__(self):
        self.max_level = 3
        self.overworld = Overworld(3, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = "level"

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level
        )
        self.status = "overworld"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()


# Pygame Setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
bg_list = import_folder("../OverworldMap")
bg_index = 0
bg_width = bg_list[bg_index].get_width()
bg_height = bg_list[bg_index].get_height()
game = Game()


while True:
    keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    bg_index += 0.1
    if bg_index >= len(bg_list):
        bg_index = 0

    screen.fill("black")
    screen.blit(
        bg_list[int(bg_index)],
        ((screen_width - bg_width) / 2, (screen_height - bg_height) / 2),
    )
    game.run()

    pygame.display.update()
    clock.tick(30)

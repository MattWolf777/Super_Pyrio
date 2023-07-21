import pygame, sys
from settings import *
from game_data import *
from level import Level
from overworld import Overworld, Icon
from support import import_folder
from UI import UI
from menu import MainMenu


class Game:
    """
    The core class representing the game. Manages game flow, level creation, player lives, coins, and UI display.

    Attributes:
        max_level (int): The maximum level the player can access.
        current_lives (int): The number of lives the player currently has.
        coins (int): The number of coins the player has collected.
        menu (MainMenu): An instance of the MainMenu class representing the game's main menu.
        status (str): A string indicating the current game status ("menu", "overworld", or "level").
        overworld (Overworld): An instance of the Overworld class representing the game's overworld map.
        ui (UI): An instance of the UI class managing the user interface display.
    """

    def __init__(self):
        # ATTRIBUTES
        self.max_level = 4
        self.current_lives = 5
        self.coins = 0

        # MENU
        self.menu = MainMenu(screen, self.create_overworld)
        self.status = "menu"

        # OVERWORLD
        self.overworld = Overworld(
            0, self.max_level, screen, self.create_level, self.create_menu
        )

        # UI
        self.ui = UI(screen)

    def create_level(self, current_level):
        """
        Creates a new Level instance for the specified current level.

        Parameters:
            - current_level (int): The index of the current level to create.

        """
        self.level = Level(
            current_level,
            screen,
            self.create_overworld,
            self.change_lives,
            self.change_coins,
        )
        self.status = "level"

    def create_overworld(self, current_level, new_max_level, player_state):
        """
        Creates a new Overworld instance based on the current level, maximum level, and player state.

        Parameters:
            current_level (int): The current level index to start from in the overworld.
            new_max_level (int): The updated maximum level the player can access.
            player_state (str): The state of the player ("small", "big", etc.).

        """
        self.player_state = player_state
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(
            current_level, self.max_level, screen, self.create_level, self.create_menu
        )
        self.status = "overworld"

    def change_lives(self, amount):
        """
        Updates the player's current lives by the specified amount. Resets the game if lives reach zero.

        Parameters:
            -amount (int): The amount to change the current lives by.

        """
        self.current_lives += amount
        if self.current_lives == 0:
            self.max_level = 1
            self.coins = 0
            self.current_lives = 5
            self.create_overworld(0, self.max_level, "small")

    def change_coins(self, amount):
        """
        Updates the player's coin count by the specified amount. Grants an extra life if coins reach 100.

        Parameters:
            amount (int): The amount to change the coin count by.

        """
        self.coins += amount
        if self.coins == 100:
            self.change_lives(1)
            self.coins = 0

    def create_menu(self):0
        """
        Creates a new MainMenu instance, transitioning the game status to the main menu.
        """
        self.menu = MainMenu(screen, self.create_overworld)
        self.status = "menu"

    def run(self):
        """
        The main game loop method. Updates the game based on its current status, running either the overworld,
        main menu, or level based on the game state.
        """

        if self.status == "overworld":
            self.overworld.run()
            self.ui.show_lives(self.current_lives)
            self.ui.show_coins(self.coins)
        elif self.status == "menu":
            self.menu.run()
        else:
            self.level.run()
            self.ui.show_lives(self.current_lives)
            self.ui.show_coins(self.coins)


# Pygame Setup
# Initialize the Pygame library.
pygame.init()

# Import a list of background images from the "../OverWorld/OverworldMap" folder.
bg_list = import_folder("../OverWorld/OverworldMap")

# Initialize the index for the current background image to be displayed.
bg_index = 0

# Create the game window using the specified screen_width and screen_height.
screen = pygame.display.set_mode((screen_width, screen_height))

# Create a clock object to manage the game's frame rate.
clock = pygame.time.Clock()

# Create an instance of the Game class to represent the core game logic.
game = Game()

# Main Game Loop
# The game loop runs continuously to keep the game running.
while True:
    # Event Handling
    # Check for any user events, such as quitting the game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Retrieve the current level index from the overworld object in the game.
    level_index = game.overworld.current_level

    # Run the game logic and update the game state.
    game.run()

    # Update the game window to reflect the changes made during the game loop iteration.
    pygame.display.update()

    # Limit the frame rate to 60 frames per second (FPS).
    clock.tick(60)

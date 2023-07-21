import pygame
from settings import screen_width, screen_height


class UI:
    """
    Represents the User Interface (UI) in the game.

    - This class manages and displays UI elements, such as the player's lives and coin count,
      on the specified surface.

    Methods:
        - show_lives(current)
        - show_coins(amount)
    """

    def __init__(self, surface):

        # SETUP
        self.display_surface = surface

    def show_lives(self, current):
        """
        Displays the player's remaining lives on the UI.

        Parameters:
            current (int): The current number of lives of the player.
        """

        self.life_panel_surface = pygame.surface.Surface((150, 70), pygame.SRCALPHA)
        self.life_panel_font = pygame.font.Font(
            "../Packages/Fonts/Super-Mario-Bros.ttf", 40
        )

        self.head_icon = pygame.image.load("../Packages/UI/head_icon.png")
        self.head_icon.set_colorkey((0, 0, 0))
        self.life_panel_surface.blit(self.head_icon, (0, 0))

        self.lives_text_surf = self.life_panel_font.render(f"x{current}", True, "White")
        self.life_panel_surface.blit(self.lives_text_surf, (70, 10))

        self.display_surface.blit(self.life_panel_surface, (50, 30))

    def show_coins(self, amount):
        """
        Displays the player's current coin count on the UI.

        Parameters:
            amount (int): The current number of coins collected by the player.
        """

        self.coin_panel_surface = pygame.surface.Surface((200, 70), pygame.SRCALPHA)
        self.coin_panel_font = pygame.font.Font(
            "../Packages/Fonts/Super-Mario-Bros.ttf", 40
        )

        self.coin_icon = pygame.image.load("../Packages/Textures/map/objects/coin.png")
        self.coin_icon.set_colorkey((0, 0, 0))
        self.coin_panel_surface.blit(self.coin_icon, (0, 0))

        # Format the coin count to be displayed with leading zeroes
        self.coin_text_surf = self.coin_panel_font.render(
            f"{(3 - len(str(amount))) * '0'}{amount}", True, "White"
        )
        self.coin_panel_surface.blit(self.coin_text_surf, (60, 00))

        # Display the coin panel on the UI at the appropriate position
        self.display_surface.blit(self.coin_panel_surface, (screen_width - 230, 30))

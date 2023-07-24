import pygame
from support import import_folder
from settings import screen_width, screen_height


class MainMenu:
    def __init__(self, screen, create_overworld):
        """
        Constructor method for the MainMenu class. Initializes the main menu with the specified attributes.

        Parameters:
            screen (pygame.Surface): The display surface where the main menu will be rendered.
            create_overworld (function): A function reference to create the overworld.

        Attributes:
            display_surface (pygame.Surface): The display surface where the main menu will be rendered.
            create_overworld (function): A function reference to create the overworld.
            background_frames (list): A list of background frames for the main menu background animation.
            bg_index (float): The current index of the background frame being displayed.
            monitor_frames (list): A list of frames for the monitor animation.

        """
        self.display_surface = screen
        self.create_overworld = create_overworld

        # Main Menu Background
        self.background_frames = import_folder("Menu/background_frames")
        self.bg_index = 0
        self.monitor_frames = import_folder("Menu/monitor_frames")

    def draw_background(self):
        """
        Draws the background animation of the main menu.
        - The background is cycled through with a slight animation.
        """
        self.bg_index += 0.2
        if self.bg_index >= len(self.background_frames):
            self.bg_index = 0
        image = pygame.transform.scale(
            self.background_frames[int(self.bg_index)], (screen_width, screen_height)
        )
        self.display_surface.blit(image, (0, 0))

        self.display_surface.blit(
            pygame.transform.scale(self.monitor_frames[int(self.bg_index)], (190, 165)),
            (520, 535),
        )

    def draw_menu_text(self):
        """
        Draws the menu text on the main menu.
        - The menu text prompts the player to "press space" to start the game.
        """
        self.menu_text_surface = pygame.surface.Surface((500, 70), pygame.SRCALPHA)
        self.menu_font = pygame.font.Font("Packages/Fonts/Super-Mario-Bros.ttf", 40)

        self.menu_text = self.menu_font.render(f"press space", True, "White")
        self.menu_text_surface.blit(self.menu_text, (70, 10))

        self.display_surface.blit(
            self.menu_text_surface, (screen_width / 2 - 250, screen_height - 80)
        )

    def draw_menu_title(self):
        """
        Draws the title image on the main menu.
        - The title image is loaded and displayed at the top center of the main menu.
        """
        self.title = pygame.image.load("Menu/menu_title.png")
        self.display_surface.blit(self.title, (screen_width / 2 - 200, 80))

    def get_input(self):
        """
        Gets the player input from the keyboard.
        - If the player presses the space key, the create_overworld function is called to start the active game cycle.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.create_overworld(0, 0, "small")

    def run(self):
        """
        Main loop for running the main menu.
        - This method is responsible for handling input, rendering the menu, and starting the game.
        """
        self.get_input()
        self.draw_background()
        self.draw_menu_text()
        self.draw_menu_title()

import pygame
from support import import_cut_graphics
import random


class Tile(pygame.sprite.Sprite):
    """
    Represents a tile entity in the game.
    - Basic tiles are just rectangular entities, they do not have an appearance.
    - They are mostly extended by other tile classes, or used as invisible detectors
      (such as goal tiles, that make the player win when touched).

    - Attributes:
        - image: An empty pygame.Surface.
        - rect: A pygame.Rect representing the position and size of the tile on the game screen.

    - Methods:
        - __init__(self, size, x, y, surface)
        - update(self, shift)


    """

    def __init__(self, size, x, y):
        """
        Initializes a new Tile instance.

        Parameters:
            size (tuple): A tuple (width, height) representing the size of the tile.
            x (int): The x-coordinate of the top-left corner of the tile.
            y (int): The y-coordinate of the top-left corner of the tile.

        Returns:
            None
        """
        super().__init__()

        # Create the tile image and set its position
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        """
        Updates the tile's position by moving it horizontally, when screen-scrolling.

        Parameters:
            shift (int): The amount to move the tile's position horizontally.

        Returns:
            None
        """
        self.rect.x += shift


class StaticTile(Tile):
    """
    Represents a static tile entity in the game.
    - This class extends the `Tile` class and represents a static tile in the game world.
    - Static tiles have texture, and they can be collided with.
    - Static Tiles are the fundamental building blocks of the levels.

    - Attributes:
        - image: A pygame.Surface representing the image or appearance of the static tile.
        - rect: A pygame.Rect representing the position and size of the static tile on the game screen.

    - Methods:
        - __init__(self, size, x, y, surface):  Constructor method for the Background class. Initializes a Static tile with the specified image, size, and position.
    """

    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)

        # Set the image of the static tile
        self.image = surface


class Background(StaticTile):
    def __init__(self, path, size, x, y):
        """
        Represents a background image displayed as a non-interactive, static element in the game.

        - Attributes:
            path (str): The file path of the image to be used as the background.
            size (tuple): A tuple containing the width and height of the background image.
            x (int): The x-coordinate position of the top-left corner of the background image.
            y (int): The y-coordinate position of the top-left corner of the background image.

        - Methods:
            __init__(self, path, size, x, y): Constructor method for the Background class. Initializes a background tile with the specified image, size, and position.
        """
        super().__init__(size, x, y, pygame.image.load(path).convert_alpha())
        offset_x = x + size[0]
        offset_y = y + size[1]
        self.rect = self.image.get_rect(bottomleft=(offset_x, offset_y))


class AnimatedTile(Tile):
    """
    Represents an animated tile with changing images over time.
    - This class extends the functionality of the Tile class, allowing you to create animated tiles with a sequence of images.

    - Attributes:

        size (tuple): A tuple containing the width and height of the animated tile.
        x (int): The x-coordinate position of the top-left corner of the animated tile.
        y (int): The y-coordinate position of the top-left corner of the animated tile.
        sprite_start_index (int): The index of the starting frame in the image sequence.
        path (str): The file path of the image sequence used for animation.
        type (str): The type of animated tile to distinguish behaviour (e.g. "coin-block").
        frame_count (int): The number of animation frames.

    - Methods:
        __init__(self, size, x, y, sprite_start_index, path, type, frame_count)
        bumped(self, strength)
        get_information(self)
        animate(self)
        update(self, shift)
    """

    def __init__(self, size, x, y, sprite_start_index, path, type, frame_count):
        super().__init__(size, x, y)
        self.start_frame_index = sprite_start_index
        self.frame_count = frame_count
        self.frames = import_cut_graphics(path, type)
        self.frame_index = self.start_frame_index
        self.image = self.frames[self.frame_index]
        self.pos = (self.rect.y, self.rect.x)
        self.type = type

        if self.type == "coin-block":
            self.coin_count = random.randint(1, random.randint(3, 16))
        else:
            self.coin_count = 1

    def bumped(self, strength):
        """
        Handles the behavior when the animated tile is bumped (jumped into from underneath)

        Parameters:
            strength (int): The strength of the bump.
        """
        if self.coin_count > 0:
            self.rect.y += strength
            self.coin_count -= 1
        if self.coin_count == 0:
            self.image = pygame.image.load(
                "../Packages/Textures/map/blocks/static/empty_question_block.png"
            )
            self.image.set_colorkey((0, 0, 0))

    def get_information(self):
        """
        Get information about the animated tile.

        Returns:
            tuple: A tuple containing the coin count and type of the animated tile.
        """
        return self.coin_count, self.type

    def animate(self):
        """Animates the tile by updating its frame index and image accordingly."""
        if self.coin_count > 0:
            self.frame_index += 0.1
            if self.frame_index > self.start_frame_index + self.frame_count:
                self.frame_index -= self.frame_count
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        """
        Moves and animates the tiles.

        Parameters:
            shift (int): The value to move the tile's position horizontally.
        """
        self.animate()
        self.rect.x += shift
        if self.rect.y < self.pos[0]:
            self.rect.y += 4
        else:
            self.rect.y = self.pos[0]

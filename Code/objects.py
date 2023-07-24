import pygame
from player import Player


class Object(pygame.sprite.Sprite):
    """
    Represents a basic game object.

    - This class extends the pygame.sprite.Sprite and provides the foundation for other game objects by handling animation
      and updating their positions on the screen.

    - Attributes:
        rect: A pygame.Rect representing the position and size of the object.

    - Methods:
        __init__(self, pos): Initializes the object with a given position.
        animate(self, speed): Animates the object by moving it upward based on the specified speed.
        update(self, shift): Updates the object's position by moving it horizontally, when screen-scrolling.
    """

    def __init__(self, pos):
        super().__init__()
        self.rect = pygame.Rect(pos, (0, 0))

    def animate(self, speed):
        """Animates the object by moving it upward based on the specified speed."""
        self.rect.y += -1 * speed

    def update(self, shift):
        """Updates the object's horizontal position based on the given shift value."""
        self.rect.x += shift


class Coins(Object):
    """
    Represents a coin object in the game.

    This class extends the Object class and adds attributes and behavior specific to coins.

    Attributes:
        - duration: The duration for which the coin remains active.
        - image: The image of the coin.
        - rect: A pygame.Rect representing the position and size of the coin.

    Methods:
        - __init__(self, pos): Initializes the coin at the specified position.
        - Methods of the Object class
    """

    def __init__(self, pos):
        super().__init__(pos)
        self.duration = 4
        self.image = pygame.image.load("Packages/Textures/map/objects/coin.png")
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos


class PowerUp(Object):
    """
    Represents a power-up object in the game.

    This class extends the Object class and adds attributes and behavior specific to power-ups.

    Attributes:
        - duration: The duration for which the power-up remains active.
        - image: The image of the power-up.
        - rect: A pygame.Rect representing the position and size of the power-up.

    Methods:
        - __init__(self, pos, player_size): Initializes the power-up at the specified position and for a given player size.
        - Methods of the Object class.
    """

    def __init__(self, pos, player_size):
        super().__init__(pos)
        if player_size == "small":
            self.image = pygame.image.load(
                "Packages/Textures/map/objects/mushroom.png"
            )
        else:
            self.image = pygame.image.load(
                "Packages/Textures/map/objects/fire-flower.png"
            )

        self.duration = 60
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pos

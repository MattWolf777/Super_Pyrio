import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    """
    Represents an enemy entity in the game.

    This class extends the AnimatedTile class and manages the behavior and attributes of an enemy character in the game.
    The enemy can move, change direction, get stunned, and be burned. It has animation frames for various states.

    Attributes:
        - speed: The speed at which the enemy moves.
        - state: The current state of the enemy (e.g., "alive", "stunned", "burned").
        - bounce_height: The height of the bounce when the enemy is stunned or burned.
        - rotation_angle: The angle of rotation when the enemy is stunned or burned.
        - y: The initial vertical position of the enemy.

    Methods:
        - __init__(self, size, x, y, sprite_start_index, path, type, frame_count)
        - move(self)
        - reverse_image(self)
        - reverse(self)
        - stumped(self)
        - stun(self)
        - get_state(self)
        - burn(self, direction)
        - update(self, shift)
    """

    def __init__(self, size, x, y, sprite_start_index, path, type, frame_count):
        """Initializes an enemy with specified attributes."""
        super().__init__(size, x, y, sprite_start_index, path, type, frame_count)
        self.speed = randint(3, 5)
        self.state = "alive"
        self.bounce_height = -10
        self.rotation_angle = 5
        self.y = y

    def move(self):
        """
        Moves the enemy horizontally and applies bouncing animations when stunned or burned.

        Updates the enemy's horizontal position based on its current speed attribute.
        If the enemy is in the "stunned" state, it performs a bouncing animation, then proceeds to walk.
        If the enemy is in the "burned" state, it bounces and falls off screen..

        Notes:
            - The enemy's state can be "alive", "stunned", or "burned".
            - The bounce_height attribute controls the height of the bounce during animations.
            - The rotation_angle attribute controls the angle of rotation during animations.
            - The self.y attribute stores the initial vertical position of the enemy before any bouncing animation.
        """
        self.rect.x += self.speed

        if self.state == "stunned":
            if self.rect.y < self.y:
                self.rect.y += self.bounce_height
                self.bounce_height += 0.3
                self.image = pygame.transform.rotate(self.image, self.rotation_angle)
                self.rotation_angle += 10
            else:
                self.rect.y = self.y
                self.speed = 3
                self.state = "alive"
                self.bounce_height = -10
                self.rotation_angle = 0

        if self.state == "burned":
            self.rect.y += self.bounce_height
            self.bounce_height += 0.3
            self.image = pygame.transform.rotate(self.image, self.rotation_angle)
            self.rotation_angle += 10

    def reverse_image(self):
        """Reverses the enemy's image horizontally."""
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """Reverses the enemy's movement direction."""
        self.speed *= -1

    def stumped(self):
        """
        Transitions the enemy to the "stumped" state, disabling movement and rendering it inactive.
        This method is called when the player jumps on the enemy.
        """
        if self.alive and self.state != "stunned":
            self.start_frame_index += 2
            self.frame_count = 1

            self.state = "stumped"
            self.rect.size = (0, 0)
            self.alive = False

    def stun(self):
        """Stuns the enemy, rendering it temporarily immobile."""
        if self.alive:
            self.state = "stunned"
            self.rect.y -= 5
            self.speed = 0

    def get_state(self):
        """Returns the current state of the enemy."""
        return self.state

    def burn(self, direction):
        """
        Sets the enemy's status to "burned".
        The enemy's vertical position, increases, and the image rotates slightly to simulate a bouncing motion.
        Then the enemy falls off screen

        Parameters:
            - direction (str): The direction in which the enemy should move ("right" or "left").
        """
        if self.alive:
            self.state = "burned"
            self.rect.y -= 5
            self.rect.size = (0, 0)
            self.alive = False
        if direction == "right":
            self.speed = 8
        else:
            self.speed = -8

    def update(self, shift):
        """Updates the enemy's position and animation."""
        self.rect.x += shift
        self.animate()
        if self.state != "stumped":
            self.move()
            self.reverse_image()

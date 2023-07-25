import pygame
from support import import_folder, import_states
import settings


class Player(pygame.sprite.Sprite):
    """
    The Player class represents the main player character in the game.

    Attributes:

        - Animation
            alive: A boolean to track if the player is alive
            frame_index: The index of the playyer animation frame that should be drawn
            animation_speed: The player animation is incremented by this much every frame.
            player_size: The size of the player rect in pixels
            last_attack_time = Tracks when the player last attacked
            combo_treshold: The maximum amount of time that can elapse between combo attacks.
            dispaly_surface: The surface, the Player should be displayed upon

        - Particles
            particle_pos: The coordinates of the particle
            particle_speed: The move speed of the attack particles

        - Player Movement
            direction: A vector representing the direction and speed of the player
            position: The coordinates of the player
            speed: The move speed of the player
            gravity: A number, the player is constantly accelerated by downwards
            jump_speed: Determines the height of the player jump

        - Player Status
            status: Represents the current status (e.g. idle, jump, attack...) of the player
            facing_right: A boolean to check in which direction the player is facing
            form: Tracks the form (small/big/fire) of the player
            crouching: A boolean to check if the player is crouching
            animation_lock: This enables/disables the player animation. While true, the animation freezes
            combo_count: To determine the attack frame
            bounced: To check if player bounced

        - Initial:
            self.image: The image of the player.
            self.rect: The hitbox of the player.

    Methods:
        import_character_asstes(self)
        animate(self)
        attack_particles(self)
        get_input(self)
        set_status(self)
        apply_gravity(self)
        update(self)
    """

    def __init__(self, pos, surface):

        super().__init__()

        # Player animation
        self.alive = True
        self.frame_index = 0
        self.animation_speed = 0.25
        self.player_size = settings.player_size
        self.last_attack_time = 0
        self.combo_treshold = 70
        self.dispaly_surface = surface

        # Player Movement
        self.direction = pygame.math.Vector2(0, 0.01)
        self.position = pygame.math.Vector2(pos[0], pos[1])
        self.speed = 5
        self.gravity = 0.6
        self.jump_speed = -18

        # Player Status
        self.status = "idle"
        self.facing_right = True
        self.form = "small"
        self.crouching = False
        self.animation_lock = False
        self.combo_count = 1
        self.bounced = False

        # Particles
        self.particle_pos = (0, 0)
        self.particle_speed = 80

        # Import assets
        self.import_character_asstes()
        self.image = pygame.transform.scale(
            self.forms[self.form]["idle"][self.frame_index], self.player_size
        )
        self.rect = self.image.get_rect(bottomleft=pos)

    def import_character_asstes(
        self,
        character_dir="../Packages/Textures/player/mario/",
        particles_dir="../Packages/Textures/particles/",
    ):
        """
        Import character assets and attack particles from the specified directories.

        Parameters:
            character_dir (str): The directory path for character assets (default is "Packages/Textures/player/mario/").
            particles_dir (str): The directory path for attack particles (default is "Packages/Textures/particles/").
        """
        # Import character assets
        self.forms = import_states(character_dir)

        # Import attack particles
        self.attack_part = import_folder(particles_dir)

    def animate(self):
        """
        Updates the player's displayed image for animation.

        The method adjusts animation speed and particle speed during attacks. It precomputes the animation sequence to avoid
        repeated dictionary lookups. The frame index wraps around the animation sequence for smooth looping.

        If the player faces left, the image is flipped horizontally. The final image is set for display.
        """
        if self.animation_lock:
            self.status = "attack_" + str(self.combo_count)
            self.animation_speed = 0.3
            if self.particle_speed > -30:
                self.particle_speed -= 8
        else:
            self.particle_speed = 70
        animation = self.forms[self.form][self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.animation_lock = False
            self.last_attack_time = pygame.time.get_ticks()
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image

        else:
            flipped_image = pygame.transform.flip(image, True, False)
            flipped_image.set_colorkey((0, 0, 0))
            self.image = flipped_image
        self.image.set_colorkey((0, 0, 0))

    def attack_particles(self):
        """
        - Displays attack particles based on the player's current attack status.

        - If the player is currently in an attack animation (indicated by 'attack' in the status), the method gets the
        - corresponding attack particle from the attack_part list based on the current combo count.

        - The particle's position is set based on the player's facing direction. If facing right, the particle appears on the
        - left side of the player; otherwise, it appears on the right side after being flipped horizontally.

        - The particle's colorkey is set to make the background transparent, and it is blitted on the display surface.
        """
        if "attack" in self.status:
            particle = self.attack_part[self.combo_count - 1]

            if self.facing_right:
                self.particle_pos = [
                    self.rect.centerx - self.particle_speed,
                    self.rect.centery - 10,
                ]
            else:
                self.particle_pos = [
                    self.rect.centerx - 100 + self.particle_speed,
                    self.rect.centery - 10,
                ]
                particle = pygame.transform.flip(particle, True, False)

            particle.set_colorkey((0, 0, 0))
            self.dispaly_surface.blit(particle, self.particle_pos)

    def get_input(self):
        """
        - Handles player movements and transformations based on keyboard input.
        - The method checks keyboard input to control various player actions, such as crouching, jumping, and attacking. It
        - also handles player transformations, including shrinking, growing, and acquiring fire power-up.
        """

        keys = pygame.key.get_pressed()

        # Crouching
        if keys[pygame.K_DOWN] and self.form != "small" and not self.crouching:
            PlayerMovements.crouch(self)
        elif not keys[pygame.K_DOWN] and self.crouching:
            PlayerMovements.stand_up(self)

        # Jumping
        if keys[pygame.K_UP] and self.direction.y == 0:
            PlayerMovements.jump(self, self.jump_speed)

        # Transformation
        if keys[pygame.K_1]:
            PlayerMovements.shrink(self)
        if keys[pygame.K_2]:
            PlayerMovements.grow(self)
        if keys[pygame.K_3]:
            PlayerMovements.grow(self)
            PlayerMovements.fire_power_up(self)

        # Horizontal movement
        if keys[pygame.K_RIGHT]:
            if not self.crouching:
                self.direction.x = 1
            elif self.crouching and self.direction.x > 0:
                PlayerMovements.slide(self, "right")
            self.facing_right = True
            self.bounced = False
        elif keys[pygame.K_LEFT]:
            if not self.crouching:
                self.direction.x = -1
            elif self.crouching and self.direction.x < 0:
                PlayerMovements.slide(self, "left")
            self.facing_right = False
            self.bounced = False
        else:
            if not self.bounced:
                self.direction.x = 0

        # Attack
        if keys[pygame.K_SPACE]:
            self.direction.x = 0
            if not self.animation_lock and self.form == "fire":
                if (
                    pygame.time.get_ticks() - self.last_attack_time
                    < self.combo_treshold
                ):
                    self.combo_count += 1
                    self.particle_speed = 80
                    if self.combo_count >= 4:
                        self.combo_count = 1
                else:
                    self.combo_count = 1

                self.animation_lock = True
                PlayerMovements.attack(self, self.combo_count)

    def set_status(self):
        """
        - Sets the player's status and animation speed based on their movement and direction.
        - The method determines the player's status based on their direction in the x and y coordinates.
        - It sets the appropriate animation speed for each status.
        """
        if 0 >= self.direction.y >= -1 and not self.crouching:
            if self.direction.x == 0:
                self.status = "idle"
                self.animation_speed = 0.2
            else:
                self.status = "run"
                self.animation_speed = 0.25
        else:
            self.animation_speed = 0.25
            if self.direction.y < -1:
                self.status = "jump"
            elif self.direction.y > 1:
                self.status = "fall"

        if self.crouching:
            self.status = "crouch"

        if self.status in ("fall", "jump"):
            self.position.y += self.direction.y
        self.position.x += self.direction.x

    def get_status(self):
        """
        - This method simply returns info about the player.
        - It is used by other classes such as Level.
        """
        return self.status, self.facing_right, self.form

    def apply_gravity(self):
        """
        - Applies gravity to the player's vertical movement.
        - The method efficiently updates the player's y-direction by adding the gravity value to it, which simulates the effect
        - of gravity on the player's movement. It then updates the player's vertical position accordingly.
        """

        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        """
        Runs all processes of the Player class
        """
        if self.alive:
            self.set_status()
            self.get_input()
        self.animate()


class PlayerMovements(Player):
    """
    - Extends the Player class to handle player movements and transformations.
    - This class inherits from the Player class and includes methods to manage various player movements.
    - Each method adjusts the player's attributes and status to perform the desired action.


    Attributes:
        Inherits all attributes from the Player class.

    Methods:
        - jump(self, jump_speed)
        - bounce(self, height, distance)
        - grow(self)
        - fire_power_up(self)
        - shrink(self)
        - attack(self, combo)
        - crouch(self)
        - slide(self, direction)
        - stand_up(self)
    """

    def jump(self, jump_speed):
        # Initiates a jump if the player is not crouching.
        if not self.crouching:
            self.direction.y = jump_speed

    def bounce(self, height, distance):
        # Simulates a bounce by adjusting the player's vertical and horizontal direction.
        self.direction.y = height
        self.direction.x = distance
        self.bounced = True

    def grow(self):
        # Transforms the player to 'big' if currently 'small'.
        if self.form == "small":
            self.rect = pygame.Rect(
                self.rect.left - 25,
                self.rect.top - 55,
                self.rect.width + 25,
                self.rect.height + 55,
            )
            self.form = "big"
            self.jump_speed = -20

    def fire_power_up(self):
        # Grants the player the fire power-up.
        self.form = "fire"

    def shrink(self):
        # Shrinks the player's size if not already 'small'.
        self.animation_lock = False
        self.status = "idle"
        if self.crouching:
            PlayerMovements.stand_up(self)
        if self.form != "small":
            self.rect = pygame.Rect(
                self.rect.left + 25,
                self.rect.top + 55,
                self.rect.width - 25,
                self.rect.height - 55,
            )
            self.form = "small"
            self.jump_speed = -18

    def attack(self, combo):
        # Performs an attack if the player is in 'fire' form.
        if self.form == "fire":
            self.status = "attack_" + str(combo)
            self.animation_speed = 0.3
            if self.crouching:
                PlayerMovements.stand_up(self)

    def crouch(self):
        # Sets the player to a crouching position if in 'big' or 'fire' form.
        if self.form == "big" or self.form == "fire":
            self.crouching = True
            self.status = "crouch"
            self.rect = pygame.Rect(
                self.rect.left,
                self.rect.top + 60,
                self.rect.width,
                self.rect.height - 60,
            )

    def slide(self, direction):
        # Initiates a sliding motion if in 'big' or 'fire' form.
        if self.form == "big" or self.form == "fire":
            self.status = "slide"
            if direction == "right":
                self.direction.x -= 0.02
            else:
                self.direction.x += 0.02

    def stand_up(self):
        # Transitions the player from a crouching position to a standing position.
        self.crouching = False
        self.rect = pygame.Rect(
            self.rect.left,
            self.rect.top - 60,
            self.rect.width,
            self.rect.height + 60,
        )

    def damage(self):
        # Handles player damage and form changes, returning True if player is still alive
        if self.form == "big" or self.form == "fire":
            PlayerMovements.shrink(self)
            return True
        else:
            return False

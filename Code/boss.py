import pygame
from support import import_states
import random


class Boss(pygame.sprite.Sprite):
    """
    - Represents a boss entity in the game.

    This class extends the pygame.sprite.Sprite and manages the behavior and attributes of a boss entity in the game.
    The boss has its animations, attacks, movements, and status. It can take damage and change forms during the gameplay.

    Attributes:

        - Boss animation
            frame_index: The index used for animating the boss.
            animation_speed: The speed at which the boss's animation changes.
            last_jump_time: The time of the boss's last jump.
            jump_duration: The duration duration between consecutive jumps.
            jump_interval: The range of time intervals between jumps.
            last_attack_time: The time of the boss's last attack.
            attack_duration: The duration duration between consecutive attacks.
            attack_interval: The range of time intervals between attacks.
            last_damage_taken: The time of the boss's last damage taken.
            damaged: A boolean flag indicating if the boss has taken damage.

        - Boss movement
            gravity: The gravity applied to the boss's vertical movement.
            jump_speed: The height of the jump.
            speed: The boss's movement speed.
            direction: A vector representing the boss's speed and direction.

        - Boss status
            dispaly_surface: The surface on which the boss is displayed.
            lives: The number of lives the boss has.
            alive: A boolean flag indicating if the boss is alive.
            status: The move status of the boss
            form: The form of the boss (right now there is only "mecha" form)
            position: A vector representing the boss's position.

        - Particles
            fire_ball: The image of the boss's fireball projectile.
            fire_ball_speed: The speed at which the fireball travels.
            particle_pos: The position of the attack particles.
            pow_effect: The image of the effect displayed when the boss takes damage.

        - Initial:
            self.image: The image of the boss.
            self.rect: The hitbox of the boss.



    Methods:
        - import_character_asstes(self)
        - animate(self)
        - move(self)
        - attack_particles(self)
        - set_status(self, status)
        - bump(self)
        - get_status(self)
        - apply_gravity(self)
        - update(self, shift)

    """

    def __init__(self, pos, surface):
        super().__init__()

        # Boss animation
        self.frame_index = 0
        self.animation_speed = 0.05
        self.last_jump_time = 0
        self.jump_duration = 2000
        self.jump_interval = [3000, 5000]
        self.last_attack_time = 0
        self.attack_duration = 1200
        self.attack_interval = [3000, 5000]
        self.last_damage_taken = 0
        self.damaged = False

        # Boss movement
        self.gravity = 0.6
        self.jump_speed = -16
        self.speed = 0
        self.direction = pygame.math.Vector2(0, 0.01)

        # Boss Status
        self.dispaly_surface = surface
        self.lives = 3
        self.alive = True
        self.status = "idle"
        self.form = "mecha"
        self.position = pygame.math.Vector2(pos[0], pos[1])

        # Particles
        self.fire_ball = pygame.image.load(
            "Packages/Textures/map/enemies/boss/mecha_boss_fire.png"
        )
        self.fire_ball.set_colorkey((0, 0, 0))
        self.fire_ball_speed = 8
        self.particle_pos = [0, 0]
        self.pow_effect = pygame.image.load(
            "Packages/Textures/map/enemies/boss/pow.jpg"
        )
        self.pow_effect.set_colorkey((0, 0, 0))

        # Initializing boss assets
        self.import_character_asstes()
        self.image = self.forms[self.form]["idle"][self.frame_index]
        self.rect = self.image.get_rect(bottomleft=pos)

    def import_character_asstes(self):
        """
        Imports the boss's animation_frames for different forms and statuses.
        """
        character_path = "Packages/Textures/map/enemies/boss/boss/"
        self.forms = import_states(character_path)

    def animate(self):
        """
        Animates the boss based on its current status and form.

        - The method handles the boss's animation by incrementing the frame index based on the animation speed.
        - If the frame index exceeds the total number of animation frames, it is reset to 0 to loop the animation.
        - The boss's image is updated with the current frame, and the colorkey is set to make the background transparent.
        - If the boss's lives reach 0, it initiates the 'die' movement.

        Args:
            self (Boss): The instance of the boss object.

        Returns:
            None
        """
        animation = self.forms[self.form][self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image.set_colorkey((0, 0, 0))

        if self.lives <= 0:
            BossMovements.die(self)

    def move(self):
        """
        Manages the boss's movements, jumps, and attacks based on time ticks.

        - The method handles the boss's behaviors (idling, jumping, and attacking), using time ticks to control its actions.
        - It updates the boss's status accordingly.

        - If the time ellapsed since last jump, and the boss isn't jumping, triggers a jump action from BossMovements class.

        - Similarly, If enough time ellapsed since last attack, triggers an attack action from BossMovements class.

        - If the boss is currently damaged, the pow effect is displayed at the boss's position to indicate damage

        Args:
            self (Boss): The instance of the boss object.

        Returns:
            None
        """
        tick = pygame.time.get_ticks()

        if 0 > self.direction.y < 1:
            self.status = "idle"

        if tick > self.last_jump_time + self.jump_duration and self.status != "jump":
            self.last_jump_time = tick
            BossMovements.jump(self, self.jump_speed)

        if tick > self.last_attack_time + self.attack_duration:

            self.last_attack_time = tick
            BossMovements.attack(self)

        if self.damaged and tick < self.last_damage_taken + 1000:
            self.dispaly_surface.blit(
                self.pow_effect, (self.rect.left, self.rect.top - 50)
            )

    def attack_particles(self):
        """
        - The method updates the position of the attack particles based on the fire ball speed.
        - It then displays the fire ball particles on the display surface at the updated position.

        Returns:
            List[int, int]: The updated particle position as a list of [x, y] coordinates.
        """
        self.particle_pos[0] -= self.fire_ball_speed
        self.dispaly_surface.blit(self.fire_ball, self.particle_pos)
        return self.particle_pos

    def set_status(self, status):
        """ """
        self.status = status

    def bump(self):
        """
        Decreases the boss's lives and applies damage effects after getting hit.

        - The boss can only be hit while in an "attack" state
        - The method efficiently reduces the boss's lives by one, indicating that the player hit the boss.
        - It also marks the boss as damaged and updates the last damage taken time.

        Additionally, it reduces the jump_interval and attack_interval by 1000 milliseconds make the boss more challanging.

        Args:
            self (Boss): The instance of the boss object.

        Returns:
            None
        """
        if self.status == "attack":
            self.lives -= 1
            self.last_damage_taken = pygame.time.get_ticks()
            self.damaged = True
            self.jump_interval = [i - 1000 for i in self.jump_interval]
            self.attack_interval = [i - 1000 for i in self.attack_interval]

    def get_status(self):
        """
        - This method simply returns info about the boss.
        - It is used by other classes such as Level.
        """
        return self.status, self.form

    def apply_gravity(self):
        """
        - Applies gravity to the boss's vertical movement.
        - The method efficiently updates the boss's y-direction by adding the gravity value to it, which simulates the effect
        - of gravity on the boss's movement. It then updates the boss's vertical position accordingly.
        """
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, shift):
        """
        Runs all processes of the Boss class
        """
        self.rect.x += shift
        self.particle_pos[0] += shift
        if self.lives > 0:
            self.move()
        self.animate()


class BossMovements(Boss):
    def jump(self, jump_speed):
        """
        - Initiates a jump.
        - The jump duration is randomly selected within the specified jump interval.
        """
        self.jump_duration = random.randint(
            self.jump_interval[0], self.jump_interval[1]
        )
        self.direction.y = jump_speed
        self.status = "jump"

    def attack(self):
        """
        - Initiates an attack.
        - Then the attack duration is randomly selected within the specified attack interval.
        - It also resets the fire projectile to spawn from the boss.
        """
        self.attack_duration = random.randint(
            self.attack_interval[0], self.attack_interval[1]
        )
        self.particle_pos = [self.rect.centerx - 100, self.rect.centery - 60]
        self.status = "attack"
        self.fire_ball_speed = 8

    def die(self):
        """
        - Kills the boss, by making it's rect size 0.
        - This makes the boss fall out of the screen.
        """
        self.rect.y -= 4
        self.rect.size = (0, 0)

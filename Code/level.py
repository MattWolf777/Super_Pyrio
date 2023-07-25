import pygame
from support import import_csv_layout, import_cut_graphics
from settings import *
from tiles import Tile, StaticTile, Background, AnimatedTile
from enemies import Enemy
from player import Player, PlayerMovements
from objects import Coins, PowerUp
from boss import Boss
from game_data import levels


class Level(Player):
    """
    - This class is responsible for most processes, such as collision checking, creating and displaying the sprites.
    - The level layouts are created from CVS files, exported from Tiled level editor.
    - CSV files are used to generate and draw levels.

    Attributes:
        - General
            display_surface: the surface, the level should be displayed upon
            world_shift: moves all sprites, to stimulate camera movement if the player would exit the screen

        - Overworld
            create_overworld: a function to be called when the level is left
            level_data: selects the correct dataset from game_data.py
            new_max_level: for the unlocking of new levels

        - Tiles
            tile_animation speed: determines the animation speed of the animated tiles
            ...layout: the return value of the import_cvs_layout function, that processes the CSV files into lists.
            ...sprites: the return value of the create_tile_group method, that iterates over the layout list, and creates sprites accordingly.
            ...tile_list: the return value of the import_cut_graphics, that cuts the spritesheet images to 64x64 tile textures, returns them in a list

        - Player
            change_form: A method to track the form of the player between levels
            player: the sprite of the player
            alive: tracks if player is alive or not
            invincible: tracks i-frames
            damage_time: tracks when the player got damaged

        - Boss
            boss: the sprite of the boss

        - User Interface
            change_lives: The change_lives function from main
            change_coins: The change_coins function from main

        - Objects
            self.coin_sprites: A spritegroup for the coins
            self.power_up_sprites: A spritegroup for the power ups

    Methods:
        - create_tile_group(layout, type)
        - enemy_collision_reverse()
        - enemy_player_collision()
        - invincibility_timer()
        - scroll_x()
        - horizontal_collisions()
        - vertical_collisions()
        - animated_collisions()
        - boss_player_collisions()
        - projectile_collisions()
        - boss_tile_collisions()
        - animate_objects()
        - player_powerup_collisions()
        - check_death(died=False)
        - check_win()
        - run()
    """

    def __init__(
        self,
        current_level,
        surface,
        create_overworld,
        change_lives,
        change_coins,
        change_form,
        player_form,
    ):

        # overworld
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data["unlock"]

        # base
        self.display_surface = surface
        self.world_shift = 0

        self.base_tile_list = import_cut_graphics(
            "../Packages/Textures/map/blocks/static/super_mario_bros__tile_revamp_by_malice936_d5ik1aw_scaled_4x_pngcrushed (1).png",
            "terrain",
        )

        # goal
        self.goal_tile_list = import_cut_graphics(
            "../Packages/Textures/map/blocks/static/castle.png",
            "goal",
        )
        goal_layout = import_csv_layout(level_data["goal"])
        self.goal = pygame.sprite.GroupSingle()
        self.goal_sprites = self.create_tile_group(goal_layout, "goal")

        # animated
        self.tile_animation_speed = 0.2
        animated_layout = import_csv_layout(level_data["animated"])
        self.animated_sprites = self.create_tile_group(animated_layout, "animated")

        # player
        self.change_form = change_form
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.create_tile_group(player_layout, "player")
        self.player_form = player_form
        self.alive = True
        self.invincible = False
        self.damage_time = 0
        # The player's form is defaulted, to what it finished the last level with
        if self.player_form == "big":
            PlayerMovements.grow(self.player.sprite)
        elif self.player_form == "fire":
            PlayerMovements.grow(self.player.sprite)
            PlayerMovements.fire_power_up(self.player.sprite)

        # boss
        self.boss = pygame.sprite.GroupSingle()
        self.fire_ball = pygame.sprite.GroupSingle()

        # UI
        self.change_lives = change_lives
        self.change_coins = change_coins

        # objects
        self.coin_sprites = pygame.sprite.GroupSingle()
        self.power_up_sprites = pygame.sprite.GroupSingle()

        # sprite group to differenciate bouncy-tiles from normal base-tiles
        self.bounce_blocks = pygame.sprite.Group()

        # base
        self.base_tile_list = import_cut_graphics(
            "../Packages/Textures/map/blocks/static/super_mario_bros__tile_revamp_by_malice936_d5ik1aw_scaled_4x_pngcrushed (1).png",
            "terrain",
        )
        base_layout = import_csv_layout(level_data["base"])
        self.base_sprites = self.create_tile_group(base_layout, "base")

        # enemies
        goomba_layout = import_csv_layout(level_data["enemies"])
        self.goomba_sprites = self.create_tile_group(goomba_layout, "enemies")
        self.collidable_enemies = self.goomba_sprites

        # constrains
        constrains_layout = import_csv_layout(level_data["constrains"])
        self.constrains_sprites = self.create_tile_group(
            constrains_layout, "constrains"
        )

        # background_setup
        background_layout = import_csv_layout(level_data["background"])
        self.background_sprites = self.create_tile_group(
            background_layout, "background"
        )

        # collidable_tiles
        self.collidable_sprites = (
            self.base_sprites.sprites() + self.animated_sprites.sprites()
        )

    def create_tile_group(self, layout, type):
        """
        - This function iterates over the given layout list, which is a 2D list with 14 rows, each containing several hundred values.
        - The values are used to determine the image of each tile based on the tile_list, which contains textures for different tile types.
        - A value of -1 represents an empty tile.
        - The position of each tile is determined by multiplying the column and row indices by the standard size of the tiles (64).

        - Args:
                self: The Level instance
                layout: a list of values representing individual tiles of this tile layer
                type: the name of the tile layer

        - Returns:
                sprite_group: A pygame spritegroup that contains all the sprites of the tiles within the specific tile layer
        """
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "base":
                        base_surface = self.base_tile_list[int(val)]
                        sprite = StaticTile((tile_size, tile_size), x, y, base_surface)
                        if int(val) in [0, 1, 2]:
                            self.bounce_blocks.add(sprite)
                        sprite_group.add(sprite)

                    elif type == "goal":
                        goal_surface = self.goal_tile_list[int(val)]
                        sprite = StaticTile((tile_size, tile_size), x, y, goal_surface)
                        sprite_group.add(sprite)

                    elif type == "enemies":
                        if val == "B":
                            sprite = Boss((x - 50, y - 130), self.display_surface)
                            self.boss.add(sprite)
                        else:
                            enemy = enemies_by_id[str(val)]
                            sprite = Enemy(
                                (enemy["width"], enemy["height"]),
                                x - (enemy["width"] - tile_size),
                                y - (enemy["height"] - tile_size),
                                enemy["start_frame_index"],
                                "../Packages/Textures/map/enemies/enemies.png",
                                "enemy",
                                enemy["frame_count"] - 1,
                            )
                            sprite_group.add(sprite)

                    elif type == "animated":
                        block_type = "power-up-block"
                        if int(val) == 0 or int(val) == 3:
                            block_type = "coin-block"
                        sprite = AnimatedTile(
                            (tile_size, tile_size),
                            x,
                            y,
                            int(val) * 4,
                            "../Packages/Textures/map/blocks/animated/question-block.png",
                            block_type,
                            4,
                        )
                        sprite_group.add(sprite)

                    elif type == "player":
                        if val == "1":
                            sprite = Player((x, y), self.display_surface)
                            self.player.add(sprite)

                        if val == "0":
                            sprite = Tile((tile_size, tile_size), x, y)
                            self.goal.add(sprite)

                    elif type == "constrains":
                        sprite = Tile((tile_size, tile_size), x, y)
                        sprite_group.add(sprite)

                    elif type == "background":
                        if val == "1":
                            sprite = Background(
                                "../Packages/Textures/map/decor/bush.png",
                                (tile_size, tile_size),
                                x,
                                y,
                            )
                            sprite_group.add(sprite)
                        elif val == "0":
                            sprite = Background(
                                "../Packages/Textures/map/decor/cloud.png",
                                (tile_size, tile_size),
                                x,
                                y,
                            )
                            sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        """
        - This function iterates over the goomba_sprites group, which contains the enemy sprites.
        - If an enemy collides with any sprite in the constrains_sprites group (representing obstacles),
        - the enemy's movement direction is reversed.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        for enemy in self.goomba_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constrains_sprites, False):
                enemy.reverse()

    def enemy_player_collision(self):
        """
        Handles collisions between enemies and the player.

        - Retrieves the player's status and direction.
        - Checks for collisions between the player and collidable enemies.
        - Updates enemy behavior based on collision and player status.
        - Handles enemy death when the player attacks or jumps on enemy.
        - Stuns enemies when the player slides into an enemy.
        - Handles player invincibility and damage if applicable.

        Args:
            self: The Level instance.

        Returns:
            None
        """

        player = self.player.sprite
        player_status, player_right = Player.get_status(player)[:2]
        enemy_collision_list = pygame.sprite.spritecollide(
            player, self.collidable_enemies, False
        )

        for enemy in self.goomba_sprites:
            if "attack" in player_status:
                if enemy.rect.colliderect(player.rect.inflate(130, 10)):
                    direction = "right" if player_right else "left"
                    Enemy.burn(enemy, direction)
            else:
                if enemy in enemy_collision_list:
                    if player_status == "slide":
                        Enemy.stun(enemy)
                    else:
                        if player.rect.bottom <= enemy.rect.top + 40:
                            Enemy.stumped(enemy)
                            PlayerMovements.jump(player, -10)
                        else:
                            if (
                                not self.invincible
                                and Enemy.get_state(enemy) != "stunned"
                            ):
                                self.alive = PlayerMovements.damage(player)
                                if not self.alive:
                                    self.check_death(True)
                                else:
                                    self.invincible = True
                                    self.damage_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        """
        Manages the invincibility timer for the player.

        - Checks if the player is currently in an invincible state.
        - Retrieves the current time in milliseconds.
        - Compares the time elapsed since the last damage with the invincibility duration (2500 milliseconds).
        - Resets the player's invincibility state if the duration has passed.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.damage_time >= 2500:
                self.invincible = False
            self.player.sprite.image.set_alpha(140)
        else:
            self.player.sprite.image.set_alpha(255)

    def scroll_x(self):
        """
        Adjusts the world shift and player speed based on the player's horizontal position.

        - Retrieves the player's sprite, center x-coordinate, and x-direction.
        - Checks if the player is near the left or right edges of the screen.
        - Sets the world shift and player speed accordingly for smooth scrolling.
        - Resets the world shift and sets the player speed to the default value if the player is within the middle range of the screen.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width * 0.6 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_collisions(self):
        """
        Handles horizontal collisions for the player.

        - Retrieves the player's sprite and updates its horizontal position based on the direction and speed.
        - Performs horizontal collision detection with the collidable sprites.
        - Adjusts the player's position based on the collided sprite to resolve the collision.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collided_sprites = pygame.sprite.spritecollide(
            player, self.collidable_sprites, False
        )

        for sprite in collided_sprites:
            if player.direction.x > 0:
                player.rect.right = sprite.rect.left
            elif player.direction.x < 0:
                player.rect.left = sprite.rect.right

    def vertical_collisions(self):
        """
        Handles vertical collisions for the player.

        - Retrieves the player's sprite and status.
        - Iterates over the collidable sprites and checks for vertical collision with the player.
        - Adjusts the player's position and movement based on the collision and tile type.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        player = self.player.sprite
        player_state = Player.get_status(player)

        for sprite in self.collidable_sprites:
            if sprite.rect.colliderect(player.rect):

                if player.direction.y > 0 and player_state != "jump":
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    if sprite in self.bounce_blocks:
                        PlayerMovements.jump(player, -20)

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 1

    def animated_collisions(self):
        """
        Handles collisions with animated tiles for the player.

        - Retrieves the player's sprite and status.
        - Performs collision detection with the animated sprites.
        - Adjusts the player's position, direction, and triggers corresponding actions based on the collision.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        player = self.player.sprite
        self.bumped = False
        player_form = Player.get_status(player)[2]

        animated_collisions = pygame.sprite.spritecollide(
            player, self.animated_sprites, False
        )
        for sprite in animated_collisions:
            if player.direction.y < 0 and not self.bumped:
                tile_info = AnimatedTile.get_information(sprite)
                self.bumped = True
                if tile_info[0] > 0:
                    if tile_info[1] == "coin-block":
                        self.coin = Coins((sprite.rect.centerx, sprite.rect.top - 30))
                        self.coin_sprites.add(self.coin)
                        self.change_coins(1)
                    else:
                        self.power_up = PowerUp(
                            (sprite.rect.centerx, sprite.rect.bottom - 30),
                            player_form,
                        )
                        self.power_up_sprites.add(self.power_up)

                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 1
                    AnimatedTile.bumped(sprite, -14)

    def boss_player_collisions(self):
        """
        Handles collisions between the player and the boss.

        - Retrieves the player and boss sprites.
        - Retrieves the boss's status.
        - Performs collision detection between the player and the boss.
        - Adjusts the player's position and triggers corresponding actions based on the collision.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        player = self.player.sprite

        if self.boss:
            boss = self.boss.sprite
            boss_state = Boss.get_status(boss)[0]
            Boss.apply_gravity(boss)

            if boss.rect.colliderect(player.rect):
                if player.rect.bottom <= boss.rect.top + 40:
                    print(boss_state)
                    if boss_state == "attack":
                        # Damage the boss and make the player bounce
                        print("boioiong")
                        Boss.bump(boss)
                        PlayerMovements.jump(player, -16)
                    else:
                        # Bounce the player off, the boss won't get damaged
                        PlayerMovements.bounce(player, -16, -5)
                else:
                    if not self.invincible:
                        # Damages the player, and sets iframes if player is still alive
                        self.alive = PlayerMovements.damage(player)
                        if not self.alive:
                            self.check_death(True)
                        else:
                            self.invincible = True
                            self.damage_time = pygame.time.get_ticks()

    def projectile_collisions(self):
        """
        Handles collisions between projectiles (boss fireballs) and the player.

        - Retrieves the boss, player, and fireball information.
        - Checks if the player collides with a fireball.
        - Handles player invincibility and damage if applicable.

        Args:
            self: The Level instance.

        Returns:
            None
        """

        player = self.player.sprite
        if self.boss:
            boss = self.boss.sprite
            fire_ball_coordinates = Boss.attack_particles(boss)

            if not self.invincible:
                if (
                    fire_ball_coordinates[0]
                    <= player.rect.right
                    <= fire_ball_coordinates[0] + 120
                    and fire_ball_coordinates[1] - 50
                    <= player.rect.top
                    <= fire_ball_coordinates[1] + 50
                ):
                    # Damages the player, and sets iframes if player is still alive
                    self.alive = PlayerMovements.damage(player)
                    if not self.alive:
                        self.check_death(True)
                    else:
                        self.invincible = True
                        self.damage_time = pygame.time.get_ticks()

    def boss_tile_collisions(self):
        """
        Handles collisions between the boss and tiles.

        - Retrieves the boss sprite.
        - Applies gravity to the boss.
        - Iterates over the collidable sprites and checks for collisions with the boss.
        - Adjusts the boss's position if a collision occurs.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        boss = self.boss.sprite

        for sprite in self.collidable_sprites:
            if sprite.rect.colliderect(boss.rect):
                # Adjust boss position if colliding from above, so boss stands on tile
                if boss.direction.y > 0:
                    boss.rect.bottom = sprite.rect.top
                    boss.direction.y = 0

    def animate_objects(self):
        """
        Animates objects in the game.

        - Draws the coin sprites on the display surface if the coin sprites list is not empty.
        - Updates the position of the coin object based on the world shift.
        - Animates the coin while animation duration is greater than 0
        - Empties the coin_sprites list if the coin animation duration reaches 0.

        - Draws the power-up sprites on the display surface if the power-up sprites list is not empty.
        - Updates the position of the power-up object based on the world shift.
        - Animates the power-up if the power-up animation duration is greater than 0.

        Args:
            self: The instance of the class that calls this method.

        Returns:
            None
        """
        if len(self.coin_sprites) != 0:
            self.coin_sprites.draw(self.display_surface)
            self.coin.update(self.world_shift)
            if self.coin.duration > 0:
                self.coin.animate(15)
                self.coin.duration -= 1
            else:
                self.coin_sprites.empty()

        if len(self.power_up_sprites) != 0:
            self.power_up_sprites.draw(self.display_surface)
            self.power_up.update(self.world_shift)
            if self.power_up.duration > 0:
                self.power_up.animate(1)
                self.power_up.duration -= 1

    def player_powerup_collisions(self):
        """
        Handles collisions between the player and power-ups.

        - Retrieves the player sprite and player size.
        - Checks for collisions between the player and power-up sprites.
        - Applies the corresponding power-up effect based on the player's size.
        - Empties the power-up sprites group.

        Args:
            self: The Level instance.

        Returns:
            None
        """
        player = self.player.sprite
        player_size = Player.get_status(player)[2]
        power_ups = pygame.sprite.spritecollide(player, self.power_up_sprites, False)

        if power_ups:
            if player_size == "big":
                PlayerMovements.fire_power_up(player)
            elif player_size == "small":
                PlayerMovements.grow(player)

            self.power_up_sprites.empty()

    def check_death(self, died=False):
        """
        Checks if the player has died and initiates appropriate actions.

        - Checks if the player has fallen off the screen or explicitly died.
        - Exits the level and loads the overworld.
        - Adjusts the player's lives count.

        Args:
            self: The Level instance.
            died (bool, optional): Indicates if the player explicitly died. Defaults to False.

        Returns:
            None
        """
        if self.player.sprite.rect.top > screen_height or died:
            self.player_form = "small"
            self.change_form(self.player_form)
            self.create_overworld(self.current_level, 0, player_size)
            self.change_lives(-1)

    def check_win(self):
        """
        Checks if the player has reached the goal and initiates appropriate actions.

        - Checks if the player collides with the goal sprites.
        - Creates the overworld and unlocks the next level

        Args:
            self: The Level instance.

        Returns:
            None
        """

        if pygame.sprite.spritecollide(self.player.sprite, self.goal_sprites, False):
            player_form = Player.get_status(self.player.sprite)[2]
            self.change_form(player_form)
            self.create_overworld(self.current_level, self.new_max_level, player_size)

    def run(self):
        """
        - Runs all processes of the Level class.
        - Updates and draws all tiles and other assets
        """

        # Background
        level_background_color = levels[self.current_level]["background_color"]
        self.display_surface.fill(level_background_color)
        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)

        # Base sprites
        self.base_sprites.update(self.world_shift)
        self.base_sprites.draw(self.display_surface)

        # Goal sprites
        self.goal_sprites.update(self.world_shift)
        self.goal_sprites.draw(self.display_surface)
        self.goal.update(self.world_shift)

        # Enemies sprites
        self.enemy_player_collision()
        self.enemy_collision_reverse()
        self.goomba_sprites.draw(self.display_surface)
        self.goomba_sprites.update(self.world_shift)
        self.constrains_sprites.update(self.world_shift)

        # Animated block sprites
        self.animated_sprites.update(self.world_shift)
        self.animated_sprites.draw(self.display_surface)

        # Player
        self.check_death()
        self.check_win()
        if self.alive:
            self.horizontal_collisions()
            self.player.sprite.apply_gravity()
            self.player_powerup_collisions()
            self.animated_collisions()
            self.projectile_collisions()
            self.vertical_collisions()

            self.scroll_x()
            Player.attack_particles(self.player.sprite)
            self.invincibility_timer()

            self.player.update()
            self.player.draw(self.display_surface)

        # Object sprites
        self.animate_objects()

        # Boss
        if self.boss:
            self.boss_player_collisions()
            self.boss_tile_collisions()
            self.boss.update(self.world_shift)
            self.boss.draw(self.display_surface)

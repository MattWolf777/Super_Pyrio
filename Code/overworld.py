import pygame
from game_data import levels
from support import import_folder
from settings import screen_width, screen_height


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, status, icon_speed):
        """
        Represents a node on the overworld map, indicating a level.

        Parameters:
            pos (tuple): The position of the node on the overworld map.
            status (str): The status of the node, "available" or "locked".
            icon_speed (int): The speed of the player icon.

        Attributes:
            image (pygame.Surface): The appearance of the node (red for available, black for locked).
            rect (pygame.Rect): The position and size of the node.
            detection_zone (pygame.Rect): The area where the icon can detect the node for movement.
        """
        super().__init__()
        self.image = pygame.Surface((10, 8))
        if status == "available":
            self.image.fill("red")
        else:
            self.image.fill("black")
        self.rect = self.image.get_rect(center=pos)
        self.detection_zone = pygame.Rect(
            self.rect.centerx - icon_speed / 2,
            self.rect.centery - icon_speed / 2,
            icon_speed,
            icon_speed,
        )


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        """
        Represents the player icon on the overworld map.

        Parameters:
            pos (tuple): The position of the icon on the overworld map.

        Attributes:
            pos (tuple): The position of the icon.
            image (pygame.Surface): The appearance of the player icon.
            rect (pygame.Rect): The position and size of the icon.
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(
            "../Packages/Textures/player/mario/small/idle/mario.png"
        )
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """
        Updates the position of the player icon on the overworld map.
        """
        self.rect.center = self.pos


class Overworld:
    """
    Represents the overworld map that allows the player to select levels.

    Parameters:
        - start_level (int): The index of the starting level.
        - max_level (int): The maximum level that the player has unlocked.
        - surface (pygame.Surface): The surface on which the overworld map is displayed.
        - create_level (function): A function that creates the selected level.
        - create_menu (function): A function that creates the main menu.

    Attributes:
        - display_surface (pygame.Surface): The surface on which the overworld map is displayed.
        - max_level (int): The maximum level that the player has unlocked.
        - first_level (int): The index of the first level (usually 0).
        - current_level (int): The index of the current selected level.
        - create_level (function): A function that creates the selected level when called.
        - move_direction (pygame.math.Vector2): The direction of the icon's movement.
        - speed (int): The speed at which the icon moves on the overworld map.
        - moving (bool): A boolean flag indicating if the icon is currently moving.
        - nodes (pygame.sprite.Group): A sprite group containing Node instances representing the level nodes on the map.
        - icon (pygame.sprite.GroupSingle): A sprite group containing the Icon instance representing the player icon.
        - bg_list (list): A list of background images for the overworld map.
        - bg_index (float): The current index of the background image being displayed.
        - screen_width (int): The width of the screen.
        - screen_height (int): The height of the screen.
        - create_menu (function): A function that creates the main menu when called.
    """

    def __init__(self, start_level, max_level, surface, create_level, create_menu):
        self.display_surface = surface
        self.max_level = max_level
        self.first_level = 0
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.moving = False

        # sprites
        self.setup_nodes()
        self.setup_icon()

        # background
        self.bg_list = import_folder("../OverWorld/OverworldMap")
        self.bg_index = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.create_menu = create_menu
        self.controls = pygame.image.load("../OverWorld/overworld_controls.png")

    def setup_nodes(self):
        """
        Sets up the nodes (level markers) on the overworld map.
        - The nodes are added to the 'nodes' sprite group with appropriate status (available or locked).
        - The method uses the 'levels' data to determine the status of each node based on the 'max_level'.
        """
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data["node_pos"], "available", self.speed)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data["node_pos"], "locked", self.speed)
                self.nodes.add(node_sprite)

    def draw_paths(self):
        """
        Draws the paths (lines) connecting the available nodes on the overworld map.
        - The paths are drawn in red color.
        - The method uses 'levels' data to determine which nodes are available to connect with lines.
        """
        points = [
            node["node_pos"]
            for index, node in enumerate(levels.values())
            if index <= self.max_level
        ]
        if self.max_level > 0:
            pygame.draw.lines(self.display_surface, "red", False, points, 6)

    def draw_background(self):
        """
        Draws the background of the overworld map.
        - The background images are cycled through with a slight animation.
        - The method uses the 'bg_list' containing the background images.
        """
        self.bg_index += 0.1
        if self.bg_index >= len(self.bg_list):
            self.bg_index = 0

        self.display_surface.blit(
            self.bg_list[int(self.bg_index)],
            (
                (screen_width - self.screen_width) / 2,
                (screen_height - self.screen_height) / 2,
            ),
        )
        self.display_surface.blit(self.controls, (50, 800))

    def setup_icon(self):
        """
        Sets up the player icon on the overworld map.
        - The icon is centered on the starting node, and it is added to the 'icon' sprite group.
        """
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        """
        Handles player input and controls the movement of the player icon.
        - The method detects key presses for movement (right, up, left, down) and spacebar (level selection).
        """
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT] or keys[pygame.K_UP]:
                if self.current_level < self.max_level:
                    self.move_direction = self.get_movement_data("next")
                    self.current_level += 1
                    self.moving = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_DOWN]:
                if self.current_level > self.first_level:
                    self.move_direction = self.get_movement_data("previous")
                    self.current_level -= 1
                    self.moving = True
            elif keys[pygame.K_SPACE]:
                if self.current_level == 0:
                    self.create_menu()
                else:
                    self.create_level(self.current_level)

    def get_movement_data(self, target):
        """
        Calculates the movement direction (vector) for the player icon between two nodes.

        Parameters:
            - target (str): The direction of movement, either "next" or "previous".

        Returns:
            - pygame.math.Vector2: The movement direction vector between the current node and the target node.
        """
        start = pygame.math.Vector2(
            self.nodes.sprites()[self.current_level].rect.center
        )

        if target == "next":
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level + 1].rect.center
            )
        else:
            end = pygame.math.Vector2(
                self.nodes.sprites()[self.current_level - 1].rect.center
            )

        return (end - start).normalize()

    def update_icon_position(self):
        """
        Updates the position of the player icon on the overworld map during movement.
        - The icon moves along the calculated movement direction until it reaches the target node.
        """
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        """
        Main loop for running the overworld map.
        - This method is responsible for handling input, updating icon position, and rendering the map.
        """
        self.input()
        self.update_icon_position()
        self.icon.update()

        self.draw_background()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)

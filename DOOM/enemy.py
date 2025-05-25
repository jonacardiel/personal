"""
enemy.py

Defines the Enemy class, inheriting from GameObject.
Includes basic AI and state management for enemies.
"""

from game_object import GameObject
from constants import TILE_SIZE, PLAYER_SPEED # Reusing PLAYER_SPEED for enemy movement for simplicity
from utils import distance, angle_between_points
import math

class Enemy(GameObject):
    """
    Represents an enemy in the game.
    """
    def __init__(self, x: float, y: float, sprite_name: str = "enemy", health: int = 100,
                 width: float = TILE_SIZE * 0.8, height: float = TILE_SIZE * 1.2):
        """
        Initializes an enemy.
        :param x: Initial X-coordinate.
        :param y: Initial Y-coordinate.
        :param sprite_name: The base name for the enemy's sprite (e.g., "imp").
        :param health: Initial health of the enemy.
        :param width: Visual width of the enemy for rendering/collision.
        :param height: Visual height of the enemy for rendering.
        """
        super().__init__(x, y, sprite_name, width, height)
        self.health = health
        self.attack_damage = 10
        self.speed = PLAYER_SPEED * 0.7 # Enemies move a bit slower
        self.state = "idle" # "idle", "walking", "attacking", "dying"
        self.target_x, self.target_y = x, y # For simple movement
        self.aggro_range = TILE_SIZE * 5 # Distance at which enemy becomes aggressive
        self.attack_range = TILE_SIZE * 1.5 # Distance at which enemy can attack

    def update(self, delta_time: float, map_data, player):
        """
        Updates the enemy's state and position.
        Implements a very basic "chase the player" AI.
        :param delta_time: Time elapsed since last update.
        :param map_data: The game map data.
        :param player: The player object.
        """
        if not self.active:
            return

        # Check distance to player
        dist_to_player = distance(self.x, self.y, player.x, player.y)

        if self.health <= 0:
            self.state = "dying"
            # In a real game, you'd play a death animation, then set active = False
            self.active = False # For now, just deactivate
            return

        if dist_to_player < self.attack_range:
            self.state = "attacking"
            # Implement attack logic here (e.g., reduce player health)
            # print(f"Enemy at ({self.x:.1f}, {self.y:.1f}) attacking player!")
        elif dist_to_player < self.aggro_range:
            self.state = "walking"
            # Simple chase: move directly towards the player
            angle_to_player = angle_between_points(self.x, self.y, player.x, player.y)
            angle_rad = math.radians(angle_to_player)

            move_x = math.cos(angle_rad) * self.speed * delta_time
            move_y = math.sin(angle_rad) * self.speed * delta_time

            new_x = self.x + move_x
            new_y = self.y + move_y

            # Basic collision check (similar to player, but simpler for enemies)
            grid_x_new = int(new_x / TILE_SIZE)
            grid_y_new = int(new_y / TILE_SIZE)

            if not map_data.is_wall_at(grid_x_new, grid_y_new):
                self.x = new_x
                self.y = new_y
            else:
                # If hitting a wall, try to slide or just stop
                # For simplicity, just stop for now
                pass
        else:
            self.state = "idle"

        # Update sprite based on state (conceptual)
        # self.sprite_name = f"{self.base_sprite_name}_{self.state}"
        # In a real game, this would involve animation frames.
        # For now, we'll just use the base sprite name for rendering.

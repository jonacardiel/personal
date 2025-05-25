"""
projectile.py

Defines the Projectile class for bullets, fireballs, etc.
"""

from game_object import GameObject
from constants import TILE_SIZE
from utils import distance
import math

class Projectile(GameObject):
    """
    Represents a projectile (e.g., bullet, fireball).
    """
    def __init__(self, x: float, y: float, angle: float, speed: float, damage: int,
                 owner_id: str, sprite_name: str = "projectile",
                 width: float = TILE_SIZE * 0.1, height: float = TILE_SIZE * 0.1):
        """
        Initializes a projectile.
        :param x: Initial X-coordinate.
        :param y: Initial Y-coordinate.
        :param angle: Angle of travel in degrees.
        :param speed: Speed of the projectile.
        :param damage: Damage dealt on hit.
        :param owner_id: Identifier of who fired the projectile (e.g., "player", "enemy_1").
        :param sprite_name: The name of the sprite for this projectile.
        :param width: Visual width of the projectile.
        :param height: Visual height of the projectile.
        """
        super().__init__(x, y, sprite_name, width, height)
        self.angle = angle
        self.speed = speed
        self.damage = damage
        self.owner_id = owner_id # To prevent self-hitting or friendly fire
        self.lifetime = 2.0 # Projectile disappears after this many seconds
        self.time_elapsed = 0.0

    def update(self, delta_time: float, map_data, player, enemies):
        """
        Updates the projectile's position and checks for collisions.
        :param delta_time: Time elapsed since last update.
        :param map_data: The game map data.
        :param player: The player object.
        :param enemies: List of active enemy objects.
        """
        if not self.active:
            return

        self.time_elapsed += delta_time
        if self.time_elapsed >= self.lifetime:
            self.active = False
            return

        # Calculate new position
        angle_rad = math.radians(self.angle)
        new_x = self.x + math.cos(angle_rad) * self.speed * delta_time
        new_y = self.y + math.sin(angle_rad) * self.speed * delta_time

        # Basic wall collision
        grid_x = int(new_x / TILE_SIZE)
        grid_y = int(new_y / TILE_SIZE)

        if map_data.is_wall_at(grid_x, grid_y):
            self.active = False # Hit a wall, deactivate
            # print(f"Projectile hit wall at ({grid_x}, {grid_y})")
            return

        self.x = new_x
        self.y = new_y

        # Check collision with enemies (if fired by player)
        if self.owner_id == "player":
            for enemy in enemies:
                if enemy.active and distance(self.x, self.y, enemy.x, enemy.y) < (self.width + enemy.width) / 2:
                    enemy.health -= self.damage
                    self.active = False # Projectile hit enemy, deactivate
                    # print(f"Projectile hit enemy! Enemy health: {enemy.health}")
                    return

        # Check collision with player (if fired by enemy)
        if self.owner_id.startswith("enemy_"):
            if distance(self.x, self.y, player.x, player.y) < (self.width + player.width) / 2:
                # player.health -= self.damage # Apply damage to player
                self.active = False # Projectile hit player, deactivate
                # print(f"Projectile hit player!")
                return

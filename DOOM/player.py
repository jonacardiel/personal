"""
player.py

Defines the Player class, handling the player's state (position, angle, speed)
and updating its movement based on input.
"""

import math
import arcade # Used for key constants

from constants import PLAYER_SPEED, PLAYER_ROTATION_SPEED, TILE_SIZE

class Player:
    """
    Represents the player in the game world.
    """
    def __init__(self, start_x: float, start_y: float, start_angle: float = 90.0):
        """
        Initializes the player.
        :param start_x: Initial X-coordinate in game units.
        :param start_y: Initial Y-coordinate in game units.
        :param start_angle: Initial angle in degrees (0 = right, 90 = up).
        """
        self.x = start_x
        self.y = start_y
        self.angle = start_angle # Angle in degrees (0-360)
        self.speed = PLAYER_SPEED # Units per second
        self.rotation_speed = PLAYER_ROTATION_SPEED # Degrees per second

    def update(self, delta_time: float, keys_pressed: set, map_data):
        """
        Updates the player's position and angle based on input and delta_time.
        Includes very basic collision detection.

        :param delta_time: Time elapsed since the last update.
        :param keys_pressed: A set of currently pressed Arcade key constants.
        :param map_data: The MapData object for collision checks.
        """
        new_x, new_y = self.x, self.y
        moved = False

        # --- Rotation ---
        if arcade.key.LEFT in keys_pressed:
            self.angle += self.rotation_speed * delta_time
            self.angle %= 360 # Keep angle within 0-360
        if arcade.key.RIGHT in keys_pressed:
            self.angle -= self.rotation_speed * delta_time
            self.angle %= 360 # Keep angle within 0-360

        # --- Movement ---
        # Convert angle to radians for trigonometric functions
        angle_rad = math.radians(self.angle)

        if arcade.key.W in keys_pressed: # Move forward
            new_x += math.cos(angle_rad) * self.speed * delta_time
            new_y += math.sin(angle_rad) * self.speed * delta_time
            moved = True
        if arcade.key.S in keys_pressed: # Move backward
            new_x -= math.cos(angle_rad) * self.speed * delta_time
            new_y -= math.sin(angle_rad) * self.speed * delta_time
            moved = True
        if arcade.key.A in keys_pressed: # Strafe left
            new_x += math.cos(angle_rad - math.pi / 2) * self.speed * delta_time
            new_y += math.sin(angle_rad - math.pi / 2) * self.speed * delta_time
            moved = True
        if arcade.key.D in keys_pressed: # Strafe right
            new_x -= math.cos(angle_rad - math.pi / 2) * self.speed * delta_time
            new_y -= math.sin(angle_rad - math.pi / 2) * self.speed * delta_time
            moved = True

        # --- Basic Collision Detection (Grid-based) ---
        # This is a very simplified collision check.
        # In a real game, you'd check against wall segments, not just grid cells.
        if moved:
            # Check collision at the new position
            grid_x = int(new_x / TILE_SIZE)
            grid_y = int(new_y / TILE_SIZE)

            if not map_data.is_wall_at(grid_x, grid_y):
                self.x = new_x
                self.y = new_y
            else:
                # If collision, try to move only along one axis to slide
                grid_x_old = int(self.x / TILE_SIZE)
                grid_y_old = int(self.y / TILE_SIZE)

                # Try X-axis movement
                if not map_data.is_wall_at(int(new_x / TILE_SIZE), grid_y_old):
                    self.x = new_x
                # Try Y-axis movement
                if not map_data.is_wall_at(grid_x_old, int(new_y / TILE_SIZE)):
                    self.y = new_y

    def get_position(self) -> tuple[float, float]:
        """Returns the player's current (x, y) coordinates."""
        return self.x, self.y

    def get_angle(self) -> float:
        """Returns the player's current angle in degrees."""
        return self.angle

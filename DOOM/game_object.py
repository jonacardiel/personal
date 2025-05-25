"""
game_object.py

Defines the base class for all dynamic objects in the game world.
Enemies, items, and projectiles will inherit from this class.
"""

class GameObject:
    """
    Base class for all interactive game objects.
    """
    def __init__(self, x: float, y: float, sprite_name: str, width: float = 0, height: float = 0):
        """
        Initializes a generic game object.
        :param x: X-coordinate of the object's center.
        :param y: Y-coordinate of the object's center.
        :param sprite_name: The name of the sprite texture to use for this object.
        :param width: The conceptual width of the object in game units.
        :param height: The conceptual height of the object in game units.
        """
        self.x = x
        self.y = y
        self.sprite_name = sprite_name # e.g., "imp_idle", "health_pack"
        self.width = width
        self.height = height
        self.active = True # Whether the object is currently active in the game

    def update(self, delta_time: float, map_data, player):
        """
        Placeholder for object-specific update logic.
        This method should be overridden by subclasses.
        :param delta_time: Time elapsed since last update.
        :param map_data: The game map data.
        :param player: The player object.
        """
        pass

    def get_position(self) -> tuple[float, float]:
        """Returns the object's current (x, y) coordinates."""
        return self.x, self.y

# No changes needed

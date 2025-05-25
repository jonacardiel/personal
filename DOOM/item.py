"""
item.py

Defines the Item class for pickups in the game (e.g., health packs, ammo).
"""

from game_object import GameObject
from constants import TILE_SIZE
from utils import distance

class Item(GameObject):
    """
    Represents a collectible item in the game world.
    """
    def __init__(self, x: float, y: float, sprite_name: str = "item", item_type: str = "health", value: int = 10):
        """
        Initializes an item.
        :param x: Initial X-coordinate.
        :param y: Initial Y-coordinate.
        :param sprite_name: The name of the sprite for this item.
        :param item_type: The type of item (e.g., "health", "ammo", "key").
        :param value: The value associated with the item (e.g., health amount, ammo count).
        """
        super().__init__(x, y, sprite_name, width=TILE_SIZE * 0.5, height=TILE_SIZE * 0.5)
        self.item_type = item_type
        self.value = value
        self.pickup_range = TILE_SIZE * 0.7 # Distance at which player can pick up

    def update(self, delta_time: float, map_data, player):
        """
        Updates the item's state (e.g., checks for player pickup).
        :param delta_time: Time elapsed since last update.
        :param map_data: The game map data.
        :param player: The player object.
        """
        if not self.active:
            return

        # Check if player is close enough to pick up
        if distance(self.x, self.y, player.x, player.y) < self.pickup_range:
            self.collect(player)

    def collect(self, player):
        """
        Applies the item's effect to the player and deactivates the item.
        :param player: The player object.
        """
        if self.item_type == "health":
            # In a real game, player would have a heal method
            # player.health += self.value
            print(f"Player collected Health Pack (+{self.value} HP)!")
        elif self.item_type == "ammo":
            # player.ammo += self.value
            print(f"Player collected Ammo (+{self.value} rounds)!")
        elif self.item_type == "key":
            # player.inventory.add_key(self.value)
            print(f"Player collected Key: {self.value}!")
        else:
            print(f"Collected unknown item type: {self.item_type}")

        self.active = False # Item is picked up and no longer active

"""
main.py

The main entry point for the PyDoom-like game.
Initializes the Arcade window, sets up the game components,
and runs the main game loop.
"""

import arcade
import os
import sys
from typing import Optional

from OpenGL.GL import glViewport, glMatrixMode, glLoadIdentity, GL_PROJECTION, GL_MODELVIEW
from OpenGL.GLU import gluPerspective

# Import custom modules
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, ASSET_DIR, PLAYER_FOV, MAX_RENDER_DISTANCE
from player import Player
from map_loader import MapLoader
from renderer import Renderer
from map_data import MapData # For type hinting

from sprite_manager import SpriteManager
from enemy import Enemy
from item import Item
from projectile import Projectile

class Game(arcade.Window):
    """
    Main game class.
    """
    def __init__(self):
        """
        Initializer for the game window.
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        if not os.path.exists(ASSET_DIR):
            print(f"Error: Asset directory '{ASSET_DIR}' not found. Please create it.")
            print("Expected structure: assets/maps/, assets/textures/, assets/sprites/")
            sys.exit(1)

        # Game components
        self.player: Optional[Player] = None
        self.map_data: Optional[MapData] = None
        self.map_loader = MapLoader()
        self.renderer: Optional[Renderer] = None
        self.sprite_manager: Optional[SpriteManager] = None

        # Input handling
        self.keys_pressed = set()
        # Load game assets and initialize components
        self.setup()

    def setup(self):
        """
        Set up the game variables. Call to restart the game.
        """
        try:
            self.map_data = self.map_loader.load_map("level1.txt")
            self.player = Player(self.map_data.player_start_x,
                                 self.map_data.player_start_y)
            self.renderer = Renderer()  # Assume Renderer can be constructed without texture manager
            # --- SpriteManager and game objects setup ---
            self.sprite_manager = SpriteManager()
            # Placeholder: Add one enemy, one item, one projectile for demonstration
            enemy = Enemy(x=128, y=128, sprite_name="enemy", health=100)
            item = Item(x=192, y=128, sprite_name="item", item_type="health", value=25)
            projectile = Projectile(x=160, y=160, angle=0, speed=100, damage=10, owner_id="player", sprite_name="projectile")
            self.sprite_manager.add_sprite(enemy)
            self.sprite_manager.add_sprite(item)
            self.sprite_manager.add_sprite(projectile)
            print("Game setup complete.")
        except FileNotFoundError:
            print("Game could not start: Map file not found. Ensure 'assets/maps/level1.txt' exists.")
            arcade.close_window()
        except Exception as e:
            print(f"An error occurred during game setup: {e}")
            arcade.close_window()

    def on_update(self, delta_time: float):
        """
        All the game logic goes here.
        :param delta_time: Time since the last update.
        """
        if self.player and self.map_data:
            self.player.update(delta_time, self.keys_pressed, self.map_data)
            # --- Update all sprites ---
            if self.sprite_manager:
                # Pass player to update for all objects
                self.sprite_manager.update(delta_time, self.map_data, self.player)
        else:
            print("Warning: Player or MapData not initialized. Skipping update.")

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        # arcade.start_render() # Not needed when using raw OpenGL calls directly

        if self.renderer and self.player and self.map_data:
            self.renderer.render_scene(self.player.x, self.player.y,
                                       self.player.angle, self.map_data,
                                       self.sprite_manager)
        else:
            # Optionally draw a loading screen or error message if not ready
            arcade.draw_text("Loading...", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.WHITE, font_size=24, anchor_x="center")

        # arcade.finish_render() # Not needed when using raw OpenGL calls directly

    def on_key_press(self, key: int, modifiers: int):
        """
        Called whenever a key is pressed.
        :param key: The key that was pressed.
        :param modifiers: Bitwise OR of modifier keys (shift, ctrl, etc.).
        """
        self.keys_pressed.add(key)

    def on_key_release(self, key: int, modifiers: int):
        """
        Called when the user releases a key.
        :param key: The key that was released.
        :param modifiers: Bitwise OR of modifier keys (shift, ctrl, etc.).
        """
        self.keys_pressed.discard(key)

    def on_resize(self, width: float, height: float):
        """
        Called when the window is resized.
        :param width: New width of the window.
        :param height: New height of the window.
        """
        super().on_resize(width, height)
        # Update OpenGL viewport and projection when window size changes
        glViewport(0, 0, int(width), int(height))
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(PLAYER_FOV, width / height, 0.1, MAX_RENDER_DISTANCE)
        glMatrixMode(GL_MODELVIEW) # Switch back to modelview for drawing

def main():
    """ Main function """
    game = Game()
    arcade.run()

if __name__ == "__main__":
    # Create necessary asset directories if they don't exist
    os.makedirs(f"{ASSET_DIR}/maps", exist_ok=True)
    os.makedirs(f"{ASSET_DIR}/textures", exist_ok=True)
    os.makedirs(f"{ASSET_DIR}/sprites", exist_ok=True)

    # --- Create a dummy map file for testing ---
    dummy_map_path = os.path.join(ASSET_DIR, "maps", "level1.txt")
    if not os.path.exists(dummy_map_path):
        print(f"Creating dummy map at: {dummy_map_path}")
        dummy_map_content = """
########
#......#
#.#P...#
#......#
########
"""
        with open(dummy_map_path, "w") as f:
            f.write(dummy_map_content.strip())

    main()

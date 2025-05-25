"""
constants.py

This file defines global constants used throughout the DOOM-like game.
Using a constants file helps centralize configuration and makes it easier
to modify game parameters.
"""

# --- Screen Dimensions ---
SCREEN_WIDTH = 1000  # Width of the game window in pixels
SCREEN_HEIGHT = 700  # Height of the game window in pixels
SCREEN_TITLE = "PyDoom-like"  # Title displayed in the window bar

# --- Game World Dimensions ---
# These represent the conceptual size of a single 'grid unit' in the 2D map
# when projected into the 3D-like view.
TILE_SIZE = 64  # Size of one map tile in game units (e.g., pixels in the 2D map)
WALL_HEIGHT = TILE_SIZE  # The height of a wall in game units

# --- Player Settings ---
PLAYER_SPEED = 150.0  # Units per second
PLAYER_ROTATION_SPEED = 100.0  # Degrees per second
PLAYER_FOV = 60.0  # Field of View in degrees

# --- Rendering Settings ---
# Number of rays to cast for rendering. More rays = higher resolution, slower performance.
NUM_RAYS = SCREEN_WIDTH
MAX_RENDER_DISTANCE = 1000.0 # Maximum distance a ray can travel

# --- Asset Paths ---
ASSET_DIR = "assets"
MAP_DIR = f"{ASSET_DIR}/maps"
TEXTURE_DIR = f"{ASSET_DIR}/textures"
SPRITE_DIR = f"{ASSET_DIR}/sprites"

# --- Colors (RGBA tuples) ---
COLOR_SKY = (0.2, 0.2, 0.7, 1.0) # Dark blue sky
COLOR_FLOOR = (0.3, 0.3, 0.3, 1.0) # Dark grey floor
COLOR_WALL_DEFAULT = (0.5, 0.5, 0.5, 1.0) # Default wall color if no texture

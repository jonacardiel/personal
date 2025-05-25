"""
map_loader.py

Handles loading the game map from a text file into a MapData object.
For simplicity, the map is a grid of characters:
'#' = wall
'.' = open space
'P' = player start position
"""

import os

from map_data import MapData, Wall
from constants import MAP_DIR, TILE_SIZE

class MapLoader:
    """
    Loads game map data from a file.
    """
    def __init__(self):
        pass

    def load_map(self, map_filename: str) -> MapData:
        """
        Loads a map from a text file and returns a MapData object.
        :param map_filename: The name of the map file (e.g., "level1.txt").
        :return: A MapData object populated with the map information.
        :raises FileNotFoundError: If the map file does not exist.
        """
        map_path = os.path.join(MAP_DIR, map_filename)
        map_data = MapData()
        player_start_found = False

        try:
            with open(map_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()] # Read non-empty lines

            if not lines:
                print(f"Warning: Map file '{map_path}' is empty.")
                return map_data

            map_data.grid_height = len(lines)
            map_data.grid_width = max(len(line) for line in lines)

            # Pad lines to ensure rectangular grid
            padded_lines = [line.ljust(map_data.grid_width, ' ') for line in lines]
            map_data.grid_map = [list(line) for line in padded_lines]

            # Iterate through the grid to identify walls and player start
            for y in range(map_data.grid_height):
                for x in range(map_data.grid_width):
                    char = map_data.grid_map[y][x]
                    if char == 'P':
                        map_data.player_start_x = (x + 0.5) * TILE_SIZE # Center in tile
                        map_data.player_start_y = (y + 0.5) * TILE_SIZE # Center in tile
                        player_start_found = True
                        map_data.grid_map[y][x] = '.' # Player start is an open space

                    # For simplicity, we're not explicitly adding Wall objects here
                    # as the renderer will infer walls from the grid_map.
                    # In a more complex system, you'd define explicit wall segments.

            if not player_start_found:
                print(f"Warning: No player start 'P' found in map '{map_filename}'. Defaulting to (0,0).")
                map_data.player_start_x = 0.5 * TILE_SIZE
                map_data.player_start_y = 0.5 * TILE_SIZE

            print(f"Map '{map_filename}' loaded successfully. Grid size: {map_data.grid_width}x{map_data.grid_height}")
            return map_data

        except FileNotFoundError:
            print(f"Error: Map file not found at '{map_path}'")
            raise
        except Exception as e:
            print(f"Error loading map '{map_path}': {e}")
            raise


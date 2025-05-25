"""
map_data.py

Defines data structures for storing map information, such as walls and sectors.
This separation helps keep the map loading and rendering logic cleaner.
"""

class Wall:
    """
    Represents a single wall segment in the 2D map.
    In a true DOOM-like, walls are often defined by two vertices (start_x, start_y)
    and (end_x, end_y), and might have different textures for front/back.
    For simplicity here, we'll represent a basic grid wall.
    """
    def __init__(self, x1: float, y1: float, x2: float, y2: float, texture_id: int = 0):
        """
        Initializes a Wall segment.
        :param x1: X-coordinate of the first point.
        :param y1: Y-coordinate of the first point.
        :param x2: X-coordinate of the second point.
        :param y2: Y-coordinate of the second point.
        :param texture_id: An ID referencing the texture for this wall.
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.texture_id = texture_id # Placeholder for texture management

class MapData:
    """
    Holds all the parsed information about the game map.
    """
    def __init__(self):
        self.grid_width: int = 0
        self.grid_height: int = 0
        self.grid_map: list[list[str]] = [] # ' ' for empty, '#' for wall
        self.walls: list[Wall] = [] # List of explicit wall segments
        self.player_start_x: float = 0.0
        self.player_start_y: float = 0.0
        # In a real DOOM-like, you'd have sectors, sprites, etc.
        # For simplicity, we'll just use a grid and infer walls.

    def add_wall(self, wall: Wall):
        """Adds a wall segment to the map data."""
        self.walls.append(wall)

    def is_wall_at(self, x: int, y: int) -> bool:
        """
        Checks if a grid cell at (x, y) contains a wall.
        Used for simple collision detection and rendering.
        """
        if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
            return self.grid_map[y][x] == '#'
        return False

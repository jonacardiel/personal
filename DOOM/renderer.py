"""
renderer.py

Handles all 2.5D rendering using PyOpenGL. This module contains the
complex logic for raycasting, drawing walls, floors, ceilings, and sprites.
"""

import math
from OpenGL.GL import *
from OpenGL.GLU import * # For gluPerspective, gluLookAt

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_FOV, TILE_SIZE, WALL_HEIGHT,
    NUM_RAYS, MAX_RENDER_DISTANCE, COLOR_SKY, COLOR_FLOOR, COLOR_WALL_DEFAULT
)
from map_data import MapData
from texture_manager import TextureManager
from sprite_manager import SpriteManager  # Add this import


class Renderer:
    """
    Manages the 2.5D rendering of the game world.
    Implements a simplified raycasting approach.
    """
    def __init__(self, texture_manager: TextureManager):
        """
        Initializes the renderer with screen dimensions and texture manager.
        :param texture_manager: An instance of TextureManager for texture access.
        """
        self.texture_manager = texture_manager
        self._setup_opengl()

        # Load some conceptual textures (these would be actual image files)
        self.wall_texture_id = self.texture_manager.load_texture("wall_brick", f"{TEXTURE_DIR}/brick.png")
        self.floor_texture_id = self.texture_manager.load_texture("floor_tile", f"{TEXTURE_DIR}/tile.png")
        self.ceiling_texture_id = self.texture_manager.load_texture("ceiling_metal", f"{TEXTURE_DIR}/metal.png")

    def _setup_opengl(self):
        """
        Sets up the initial OpenGL state for 3D rendering.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0) # Black background initially
        glEnable(GL_DEPTH_TEST) # Enable depth testing for correct drawing order
        glEnable(GL_TEXTURE_2D) # Enable 2D texturing
        glShadeModel(GL_SMOOTH) # Smooth shading
        glEnable(GL_BLEND) # Enable blending for transparency (e.g., for sprites)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Set up the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Use gluPerspective for a 3D perspective projection
        gluPerspective(PLAYER_FOV, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, MAX_RENDER_DISTANCE)

        # Set up the modelview matrix (camera)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        print("OpenGL renderer initialized.")

    def render_scene(self, player_x: float, player_y: float, player_angle: float, map_data: MapData, sprite_manager: 'SpriteManager' = None):
        """
        Renders the entire game scene from the player's perspective.
        :param player_x: Player's X-coordinate.
        :param player_y: Player's Y-coordinate.
        :param player_angle: Player's angle in degrees.
        :param map_data: The MapData object containing the map layout.
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clear color and depth buffers
        glLoadIdentity() # Reset the modelview matrix

        # --- Set up Camera (Conceptual) ---
        # In a raycaster, the camera isn't explicitly moved like this in OpenGL.
        # Instead, the rays are cast from the player's perspective, and the
        # geometry is drawn directly.
        # However, for drawing floor/ceiling or sprites, a standard camera setup helps.
        # For a true raycaster, you'd draw columns directly in 2D screen space.
        # This approach mixes 2D column drawing with some 3D elements for floor/ceiling.

        # Draw sky and floor (simple colored rectangles for now)
        self._draw_sky_and_floor()

        # --- Raycasting Loop (Conceptual) ---
        # This loop simulates casting rays for each vertical strip of the screen.
        # The actual raycasting math (DDA algorithm, etc.) is complex and
        # would go inside `_cast_ray`.

        half_fov_rad = math.radians(PLAYER_FOV / 2)
        player_angle_rad = math.radians(player_angle)

        for ray_num in range(NUM_RAYS):
            # Calculate the angle for this specific ray
            # The angle should sweep from (player_angle - FOV/2) to (player_angle + FOV/2)
            ray_angle = player_angle_rad - half_fov_rad + \
                        (ray_num / (NUM_RAYS - 1)) * (half_fov_rad * 2)

            # Perform the raycast
            hit_info = self._cast_ray(player_x, player_y, ray_angle, map_data)

            if hit_info:
                distance = hit_info['distance']
                # Correct for "fisheye" distortion by multiplying by cosine of angle difference
                corrected_distance = distance * math.cos(ray_angle - player_angle_rad)

                # Calculate the height of the wall slice on the screen
                # The further the wall, the shorter it appears.
                wall_screen_height = (WALL_HEIGHT / corrected_distance) * (SCREEN_HEIGHT / (2 * math.tan(half_fov_rad)))

                # Calculate where on the screen this wall slice should be drawn
                x_screen_pos = ray_num # The column on the screen

                # Draw the wall slice
                self._draw_wall_slice(x_screen_pos, wall_screen_height, hit_info['texture_id'], hit_info['texture_offset'])

                # In a full raycaster, you'd also draw floor/ceiling for this column
                # based on the wall hit and the remaining screen space.
                # This is simplified by drawing a single floor/sky plane earlier.

        # --- Draw Sprites (Conceptual) ---
        if sprite_manager is not None:
            self._draw_sprites(player_x, player_y, player_angle, sprite_manager)

    def _draw_sky_and_floor(self):
        """
        Draws a simple sky and floor as colored rectangles.
        In a real raycaster, these might be rendered per column or as textured planes.
        """
        glDisable(GL_TEXTURE_2D) # Disable textures for solid colors

        # Draw sky (top half of the screen)
        glColor4f(*COLOR_SKY)
        glBegin(GL_QUADS)
        glVertex2f(0, SCREEN_HEIGHT / 2)
        glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT / 2)
        glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
        glVertex2f(0, SCREEN_HEIGHT)
        glEnd()

        # Draw floor (bottom half of the screen)
        glColor4f(*COLOR_FLOOR)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(SCREEN_WIDTH, 0)
        glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT / 2)
        glVertex2f(0, SCREEN_HEIGHT / 2)
        glEnd()

        glEnable(GL_TEXTURE_2D) # Re-enable textures for walls

    def _cast_ray(self, start_x: float, start_y: float, angle_rad: float, map_data: MapData) -> dict | None:
        """
        Conceptual raycasting function.
        This would implement a DDA (Digital Differential Analyzer) algorithm
        or similar to find the first wall intersection.

        :param start_x: Ray origin X.
        :param start_y: Ray origin Y.
        :param angle_rad: Ray direction angle in radians.
        :param map_data: The map data to check for walls.
        :return: A dictionary with hit information (distance, texture_id, texture_offset)
                 or None if no wall is hit within MAX_RENDER_DISTANCE.
        """
        # --- Placeholder for complex raycasting logic ---
        # This is where the core raycasting algorithm (e.g., DDA) would go.
        # It would step along the ray, checking grid cells for walls.
        # When a wall is hit, it calculates:
        # 1. The distance to the wall.
        # 2. Which side of the wall was hit (for texture mapping).
        # 3. The exact hit point on the wall (for texture offset).
        # 4. The texture ID for that wall.

        # For this example, we'll simulate a hit at a fixed distance if a wall exists.
        # In a real raycaster, you'd iterate through grid cells:
        # current_x, current_y = start_x, start_y
        # dx = math.cos(angle_rad)
        # dy = math.sin(angle_rad)
        # while distance < MAX_RENDER_DISTANCE:
        #    # Calculate next grid intersection
        #    # Check map_data.is_wall_at(grid_x, grid_y)
        #    # If wall hit, calculate distance, texture_offset, etc.
        #    # return hit_info
        #    pass

        # Simple conceptual hit for demonstration:
        # Find the grid cell the player is currently in
        grid_x = int(start_x / TILE_SIZE)
        grid_y = int(start_y / TILE_SIZE)

        # Simulate hitting a wall if the next cell in a cardinal direction is a wall
        # This is NOT how a real raycaster works, but demonstrates the output.
        if map_data.is_wall_at(grid_x + 1, grid_y) or \
           map_data.is_wall_at(grid_x - 1, grid_y) or \
           map_data.is_wall_at(grid_x, grid_y + 1) or \
           map_data.is_wall_at(grid_x, grid_y - 1):
            # Simulate a hit at a fixed distance for demonstration
            simulated_distance = TILE_SIZE / 2 # Close wall
            return {
                'distance': simulated_distance,
                'texture_id': self.wall_texture_id,
                'texture_offset': 0.5 # Where on the texture the ray hit (0.0 to 1.0)
            }
        return None # No wall hit conceptually

    def _draw_wall_slice(self, screen_x: int, wall_screen_height: float, texture_id: int, texture_offset: float):
        """
        Draws a single vertical slice of a wall on the screen.
        :param screen_x: The X-coordinate on the screen (column).
        :param wall_screen_height: The calculated height of the wall slice in pixels.
        :param texture_id: The OpenGL texture ID to use.
        :param texture_offset: The U-coordinate (horizontal) for texture mapping (0.0 to 1.0).
        """
        # Calculate the top and bottom Y-coordinates for the wall slice
        # Center the wall slice vertically on the screen
        half_height = SCREEN_HEIGHT / 2
        top_y = half_height + wall_screen_height / 2
        bottom_y = half_height - wall_screen_height / 2

        # Bind the texture for this wall slice
        self.texture_manager.bind_texture(texture_id)
        glColor4f(1.0, 1.0, 1.0, 1.0) # Reset color to white for texture

        glBegin(GL_QUADS)
        # Bottom-left vertex
        glTexCoord2f(texture_offset, 0.0) # U, V (V=0.0 is bottom of texture)
        glVertex2f(screen_x, bottom_y)

        # Bottom-right vertex
        glTexCoord2f(texture_offset, 1.0) # U, V (V=1.0 is top of texture)
        glVertex2f(screen_x + 1, bottom_y) # Width of 1 pixel column

        # Top-right vertex
        glTexCoord2f(texture_offset, 1.0)
        glVertex2f(screen_x + 1, top_y)

        # Top-left vertex
        glTexCoord2f(texture_offset, 0.0)
        glVertex2f(screen_x, top_y)
        glEnd()

    def _draw_sprites(self, player_x, player_y, player_angle, sprite_manager: 'SpriteManager'):
        """
        Draws sprites (enemies, items) with correct projection, scaling, and depth sorting.
        :param player_x: Player's X-coordinate.
        :param player_y: Player's Y-coordinate.
        :param player_angle: Player's angle in degrees.
        :param sprite_manager: SpriteManager instance providing sprite data.
        """
        # Gather all sprites and compute distance to player
        sprites = []
        for sprite in sprite_manager.get_sprites():
            dx = sprite.x - player_x
            dy = sprite.y - player_y
            distance = math.hypot(dx, dy)
            sprites.append((distance, sprite))

        # Sort sprites by distance (farthest to nearest)
        sprites.sort(reverse=True, key=lambda tup: tup[0])

        # Precompute values for projection
        half_fov_rad = math.radians(PLAYER_FOV / 2)
        player_angle_rad = math.radians(player_angle)
        screen_dist = (SCREEN_WIDTH / 2) / math.tan(half_fov_rad)

        for distance, sprite in sprites:
            # Angle from player to sprite
            dx = sprite.x - player_x
            dy = sprite.y - player_y
            sprite_angle = math.atan2(dy, dx)
            angle_diff = (sprite_angle - player_angle_rad + math.pi) % (2 * math.pi) - math.pi

            # Only draw if within FOV
            if abs(angle_diff) > half_fov_rad:
                continue

            # Project sprite to screen
            sprite_screen_x = SCREEN_WIDTH / 2 + math.tan(angle_diff) * screen_dist

            # Scale sprite based on distance
            size = getattr(sprite, "width", TILE_SIZE * 0.5)
            if distance > 0.01:
                sprite_screen_height = (size / distance) * screen_dist
            else:
                sprite_screen_height = SCREEN_HEIGHT  # Avoid div by zero

            # Vertical position (centered)
            top_y = (SCREEN_HEIGHT / 2) + (sprite_screen_height / 2)
            bottom_y = (SCREEN_HEIGHT / 2) - (sprite_screen_height / 2)

            # Bind sprite texture (placeholder: just set color)
            glColor4f(1.0, 1.0, 1.0, 1.0)

            # Draw the sprite as a vertical quad
            glBegin(GL_QUADS)
            # Bottom-left
            glTexCoord2f(0.0, 0.0)
            glVertex2f(sprite_screen_x - sprite_screen_height / 2, bottom_y)
            # Bottom-right
            glTexCoord2f(1.0, 0.0)
            glVertex2f(sprite_screen_x + sprite_screen_height / 2, bottom_y)
            # Top-right
            glTexCoord2f(1.0, 1.0)
            glVertex2f(sprite_screen_x + sprite_screen_height / 2, top_y)
            # Top-left
            glTexCoord2f(0.0, 1.0)
            glVertex2f(sprite_screen_x - sprite_screen_height / 2, top_y)
            glEnd()

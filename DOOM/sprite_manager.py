"""
sprite_manager.py

Manages the loading and binding of sprite textures for OpenGL.
Sprites are typically 2D images with transparency that are drawn
on top of the 2.5D world.
"""

import os
# You'll need Pillow for image loading: pip install Pillow
from PIL import Image
from OpenGL.GL import *

from constants import SPRITE_DIR

class SpriteManager:
    """
    Manages loading and providing OpenGL texture IDs for sprites.
    """
    def __init__(self):
        self.sprites = {} # Stores {sprite_name: opengl_texture_id}

    def load_sprite(self, sprite_name: str, file_path: str) -> int:
        """
        Loads a sprite image and returns its OpenGL texture ID.
        Sprites are typically PNGs with alpha channels for transparency.

        :param sprite_name: A unique name for this sprite (e.g., "IMP_IDLE_1").
        :param file_path: The path to the sprite image file.
        :return: An integer ID representing the OpenGL texture, or 0 if loading fails.
        """
        if sprite_name in self.sprites:
            print(f"Sprite '{sprite_name}' already loaded.")
            return self.sprites[sprite_name]

        full_path = os.path.join(SPRITE_DIR, file_path)
        print(f"Loading sprite: {full_path}")

        gl_texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, gl_texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        try:
            # Load image with PIL, flip vertically for OpenGL, convert to RGBA
            image = Image.open(full_path).transpose(Image.FLIP_TOP_BOTTOM)
            img_data = image.convert("RGBA").tobytes()

            # Upload image data to OpenGL texture
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height,
                         0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

            self.sprites[sprite_name] = gl_texture_id
            print(f"Sprite '{sprite_name}' loaded with OpenGL ID: {gl_texture_id}")
            return gl_texture_id
        except FileNotFoundError:
            print(f"Error: Sprite file not found at {full_path}")
            return 0 # Return 0 for invalid texture
        except Exception as e:
            print(f"Error loading sprite {full_path}: {e}")
            return 0

    def get_sprite_id(self, sprite_name: str) -> int:
        """
        Returns the OpenGL texture ID for a given sprite name.
        """
        return self.sprites.get(sprite_name, 0) # Return 0 if not found

    def bind_sprite(self, sprite_id: int):
        """
        Binds an OpenGL sprite texture for drawing.
        :param sprite_id: The OpenGL ID of the sprite texture to bind.
        """
        glBindTexture(GL_TEXTURE_2D, sprite_id)

    def add_sprite(self, sprite_name: str, sprite):
        """
        Adds a new sprite to the manager.
        :param sprite_name: A unique name for this sprite.
        :param sprite: The sprite object to add.
        """
        self.sprites[sprite_name] = sprite

    def get_sprites(self):
        """
        Returns a list of active sprites.
        """
        # Return only active sprites
        return [s for s in self.sprites if getattr(s, "active", True)]

    def update(self, delta_time, map_data, player):
        """
        Updates all sprites, passing the player object for context.
        :param delta_time: The time elapsed since the last update.
        :param map_data: The current map data.
        :param player: The player object.
        """
        # Update all sprites, passing player for context
        for sprite in self.sprites:
            # For projectiles, pass enemies list if needed
            if hasattr(sprite, "update"):
                # For projectiles, pass enemies list if needed
                if sprite.__class__.__name__ == "Projectile":
                    # Pass all enemies for collision detection
                    enemies = [s for s in self.sprites if s.__class__.__name__ == "Enemy"]
                    sprite.update(delta_time, map_data, player, enemies)
                else:
                    sprite.update(delta_time, map_data, player)

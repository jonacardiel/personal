import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from wad_data import WADData
from wadreader import WADReader
from settings import *
import sys
from map_renderer import MapRenderer
import os

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 0.1
PLAYER_TURN_SPEED = 2.0 # Degrees per frame
FOV = 70 # Field of View
NEAR_CLIP = 0.1 # Near clipping plane
FAR_CLIP = 100.0 # Far clipping plane

class DoomEngine:
    def __init__(self):
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.wad_path = os.path.join(SCRIPT_DIR, 'assets', 'DOOM.WAD')
        # Check if WAD file exists before proceeding
        if not os.path.exists(self.wad_path):
            print(f"Error: WAD file not found at '{self.wad_path}'. Please ensure the file exists.")
            input("Press Enter to exit...")
            sys.exit(1)
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.running = True
        self.dt = 1/60
        self.wad_reader = WADReader(self.wad_path)
        self.map_data = self.wad_reader.map_data
        self.map_renderer = MapRenderer(self)

    def update(self):
        self.dt = self.clock.tick()
        pg.display.flip()
        pg.display.set_caption(f'{self.clock.get_fps():.2f}')

    def draw(self):
        self.screen.fill('black')
        if self.map_renderer:
            self.map_renderer.draw()
        # Draw the game world here

    def check_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    pg.init()
    doom_engine = DoomEngine()
    print(f"DOOM engine initialized with WAD path: {doom_engine.wad_path}")
    doom_engine.run()

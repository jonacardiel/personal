import pygame as pg
from settings import *

class MapRenderer:
    def __init__(self, doom_engine):
        self.doom_engine = doom_engine
        self.wad_reader = doom_engine.WADReader
        self.map_data = self.wad_reader.map_data  # Ensure map_data is assigned
        self.vertexes = self.map_data.vertexes
        self.linedefs = self.map_data.linedefs
        self.x_min, self.x_max, self.y_min, self.y_max = self.get_map_bounds()
        self.vertexes = [pg.math.Vector2(self.remap_x(v.x), self.remap_y(v.y)) for v in self.vertexes]

    def draw(self):
        self.draw_linedefs()
        self.draw_vertexes()

    def remap_x(self, n, out_min=30, out_max=WIDTH - 30):
        return int((n - self.x_min) / (self.x_max - self.x_min) * (out_max - out_min) + out_min)

    def draw_linedefs(self):
        for line in self.linedefs:
            p1 = self.vertexes[line.start_vertex_id]
            p2 = self.vertexes[line.end_vertex_id]
            pg.draw.line(self.doom_engine.screen, 'orange', p1, p2, 3)

    def remap_y(self, n, out_min=30, out_max=HEIGHT - 30):
        return int((n - self.y_min) / (self.y_max - self.y_min) * (out_max - out_min) + out_min)

    def get_map_bounds(self):
        x_sorted = sorted(self.vertexes, key=lambda v: v.x)
        x_min, x_max = x_sorted[0].x, x_sorted[-1].x

        y_sorted = sorted(self.vertexes, key=lambda v: v.y)
        y_min, y_max = y_sorted[0].y, y_sorted[-1].y
        return x_min, x_max, y_min, y_max

    def draw_vertexes(self):
        for v in self.vertexes:
            pg.draw.circle(self.doom_engine.screen, 'white', (v.x, v.y), 4)

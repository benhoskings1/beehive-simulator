from screen import Screen, Colours
from circle_coordinates import get_coordinates
from utils import *

import pygame as pg


class BeehiveDisplay:
    def __init__(self, display_size=(800, 600)):
        self.screen = Screen(size=display_size, colour=Colours.white)
        self.hive_radius = 100
        self.hive_offset = vec((self.screen.size.x - 2 * self.hive_radius) / 2,
                               (self.screen.size.y - 2 * self.hive_radius) / 2)
        self.hive_coords = get_coordinates(sides=len(activities), radius=self.hive_radius, offset=self.hive_offset)
        self.activity_coords = dict(zip(range(len(activities)), self.hive_coords))
        print(self.activity_coords)

        for activity_idx in range(len(activities)):
            pg.draw.circle(
                self.screen.base_surface,
                pg.Color(255, 0, 0, 20),
                self.activity_coords[activity_idx],
                radius=50,

            )

    def render_hive(self, activity_count):
        self.screen.refresh()
        for activity, count in activity_count.items():
            pg.draw.circle(
                self.screen.surface,
                Colours.black.value,
                self.activity_coords[activity],
                radius=count*2
            )

    def get_surface(self):
        return self.screen.get_surface()
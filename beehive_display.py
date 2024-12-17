from screen import Screen, Colours
from circle_coordinates import get_coordinates
from utils import *

import pygame as pg

class BeehiveDisplay:
    def __init__(self):
        self.screen = Screen(size=(800, 600), colour=Colours.white)
        self.hive_coords = get_coordinates(sides=len(activity_times), radius=20)
        self.activity_coords = dict(zip(activity_times.keys(), self.hive_coords))
        print(self.activity_coords)

    def render_hive(self, activity_count):
        for activity, count in activity_count:
            pg.draw.circle(
                self.screen.surface,
                Colours.black.value,
                self.activity_coords[activity],
                radius=activity_count
            )

    def get_surface(self):
        return self.screen.get_surface()
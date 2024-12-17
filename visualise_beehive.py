import pygame as pg
import time

from utils import *
from circle_coordinates import get_coordinates
from screen import Screen, Colours
from bee import Bee
from beehive import Beehive
from beehive_display import BeehiveDisplay

if __name__ == "__main__":

    pg.init()
    window = pg.display.set_mode((800, 600))
    beehive_display = BeehiveDisplay(display_size=window.get_size())

    beehive = Beehive(10,)

    window.blit(beehive_display.get_surface(), (0, 0))
    pg.display.flip()
    pg.event.pump()

    while True:
        beehive.process_iteration()
        print(beehive.activity_counts)

        beehive_display.render_hive(beehive.activity_counts)
        window.blit(beehive_display.get_surface(), (0, 0))
        pg.display.flip()
        pg.event.pump()
        time.sleep(0.1)

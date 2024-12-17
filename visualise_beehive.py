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
    beehive_display = BeehiveDisplay()

    beehive = Beehive(count=10, start_state=0)

    window.blit(beehive_display.get_surface(), (0, 0))
    pg.display.flip()
    pg.event.pump()

    while True:
        beehive.process_iteration()
        print(beehive.activity_counts)
        time.sleep(0.1)

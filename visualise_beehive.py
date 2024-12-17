import pygame as pg
import time

from utils import *
from screen import Screen, Colours
from bee import Bee

if __name__ == "__main__":

    pg.init()
    window = pg.display.set_mode((800, 600))

    screen = Screen(size=(800, 600), colour=Colours.white)

    window.blit(screen.get_surface(), (0, 0))
    pg.display.flip()
    pg.event.pump()

    bees = [Bee() for i in range(5)]

    while True:
        for bee in bees:
            bee.process_iteration()

        time.sleep(0.1)

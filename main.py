import pygame as pg
from beehive import Beehive

if __name__ == "__main__":
    print(f"Creating beehive")

    pg.init()
    window = pg.display.set_mode((1200, 800))
    beehive = Beehive(1000, display_size=window.get_size(), load_from_save=True)
    beehive.run()

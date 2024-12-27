from enum import Enum
import pygame as pg
import random


class BeeStates(Enum):
    initialise = 100
    dead = 0
    birth = 1
    sleeping = 2
    flying = 3
    gathering = 4
    unloading = 5

activity_cycle = {
    0: "Sleeping",
    1: "Flying",
    2: "Gathering",
    3: "Flying",
    4: "Unloading",
}

activity_times = {
    BeeStates.sleeping: 10,
    BeeStates.gathering: 20,
    BeeStates.birth: 10,
    BeeStates.flying: 20,
    BeeStates.unloading: 10,
}

vec = pg.Vector2





def change_opacity(colour, alpha):
    col = list(colour)
    col[3] = int(alpha)
    return pg.Color(col)
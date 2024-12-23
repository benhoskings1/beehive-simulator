from enum import Enum
import pygame as pg
import random

activities = [
    "Sleeping",
    "Flying",
    "Gathering",
    "Unloading"
]

activity_cycle = {
    0: "Sleeping",
    1: "Flying",
    2: "Gathering",
    3: "Flying",
    4: "Unloading",
}

activity_times = {
    "Sleeping": 10,
    "Gathering": 20,
    "Flying": 10,
    "Unloading": 10
}

vec = pg.Vector2


class BeeStates(Enum):
    dead = 0
    birth = 1
    sleeping = 2
    flying = 3
    gathering = 4
    unloading = 5


def change_opacity(colour, alpha):
    col = list(colour)
    col[3] = int(alpha)
    return pg.Color(col)
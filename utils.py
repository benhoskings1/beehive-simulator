import pygame as pg
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

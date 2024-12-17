import pygame as pg
activities = [
    "Sleeping",
    "Flying",
    "Gathering",
    "Flying",
    "Unloading"
]

activity_cycle = {
    idx: name for idx, name in enumerate(activities)
}

activity_times = {
    "Sleeping": 10,
    "Gathering": 20,
    "Flying": 10,
    "Unloading": 10
}

vec = pg.Vector2

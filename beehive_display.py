from screen import Screen, Colours
from circle_coordinates import get_coordinates
from utils import *
import pygame as pg
from numpy import random


class TransitionLine(pg.sprite.Sprite):
    def __init__(self, start: vec, end: vec, colour=None, deviate=True):
        super().__init__()
        self.object_type = "transition_line"
        if type(start) is not pg.Vector2:
            start = vec(end)

        if deviate:
            offset = pg.Vector2(*(10*random.randn(2, 1)))
        else:
            offset = vec(0, 0)

        start_point = start + offset

        self.rect = pg.Rect(min(start_point[0], end[0]),  min(start_point[1], end[1]),
                            max(start_point[0], end[0]) - min(start_point[0], end[0]),
                            max(start_point[1], end[1]) - min(start_point[1], end[1]))
        self.age = 1
        if colour:
            self.colour = colour.value
        else:
            self.colour = Colours.hero_blue.value

        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)
        col = change_opacity(Colours.hero_blue.value, 255 / self.age)
        pg.draw.line(
            self.image, col,
            start_point - self.rect.topleft, end - self.rect.topleft,
            width=3,
        )

    def update_image(self):
        self.image.set_alpha(255 / self.age)


class GameObjects(pg.sprite.Group):
    def __init__(self, sprites):
        super().__init__(self, sprites)

    def draw(self, surf: pg.Surface, bgsurf=None, special_flags: int = 0):
        for obj in self.sprites():
            if obj.object_type == "transition_line":
                if obj.age < 5:
                    surf.blit(obj.image, obj.rect.topleft)
                else:
                    self.remove(obj)

    def increment_age(self):
        for obj in self.sprites():
            obj.age += 1
            obj.update_image()


class BeehiveDisplay(Screen):
    def __init__(self, size, bee_count):
        super().__init__(size, colour=Colours.white)
        self.hive_radius = min(size[0], size[1]) * 0.4
        self.hive_offset = vec((self.size.x - 2 * self.hive_radius) / 2,
                               (self.size.y - 2 * self.hive_radius) / 2)
        self.hive_coords = get_coordinates(sides=len(BeeStates), radius=self.hive_radius, offset=self.hive_offset)
        self.activity_coords = dict(zip(BeeStates, self.hive_coords))
        print(self.activity_coords)

        self.sprites = GameObjects([])

        self.bee_count = bee_count

    def render_hive(self, activity_count):
        self.refresh()
        for activity, count in activity_count.items():
            pg.draw.circle(
                self.surface,
                Colours.black.value,
                self.activity_coords[activity],
                radius=100 * count/self.bee_count,
            )

    def add_new_transition(self, start_state: BeeStates, end_state: BeeStates):
        tl = TransitionLine(start=self.activity_coords[start_state],
                            end=self.activity_coords[end_state])

        self.sprites.add(tl)

    def get_surface(self):
        self.sprite_surface = pg.Surface(self.size, pg.SRCALPHA)
        self.sprites.draw(self.sprite_surface)
        display_surf = self.base_surface.copy()
        display_surf.blit(self.surface, (0, 0))
        display_surf.blit(self.sprite_surface, (0, 0))

        return display_surf

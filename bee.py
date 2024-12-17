import random
from utils import *
import time


class Bee:
    def __init__(self, state=None):
        if state:
            self.activity_id = state
        else:
            self.activity_id = random.choice(list(activity_cycle.keys()))

        self.activity_prev = None
        self.activity_time = 0

    def process_iteration(self):
        changed = False
        if self.activity_time + random.randint(-5, 5) > activity_times[activity_cycle[self.activity_id]]:
            self.activity_id = (self.activity_id + 1) % len(activity_cycle)
            self.activity_time = 0
            changed = True

        self.activity_time += 1

        if changed:
            return self.activity_id

    def print_status(self):
        print(f"Activity: {activity_cycle[self.activity_id]} \n"
              f"Time: {self.activity_time}")





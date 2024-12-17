

from bee import Bee
from utils import *


class Beehive:
    def __init__(self, count=5, start_state=0):
        self.activity_count = len(activities)
        self.bees = [Bee(state=start_state) for _ in range(count)]
        self.activity_counts = {i: 0 for i in range(len(activities))}
        for bee in self.bees:
            self.activity_counts[bee.activity_id] += 1

    def process_iteration(self):
        for bee in self.bees:
            changed_id = bee.process_iteration()
            if changed_id:
                print(changed_id)
                self.activity_counts[(changed_id - 1) % self.activity_count] -= 1
                self.activity_counts[changed_id] += 1

import numpy as np

from bee import Bee
from utils import *
import pandas as pd


class Beehive:
    def __init__(self, count=5, start_state=None):
        self.activity_count = len(activities)
        self.bees = [Bee(state=start_state) for _ in range(count)]
        self.activity_counts = {i: 0 for i in range(len(activity_cycle))}
        for bee in self.bees:
            self.activity_counts[bee.activity_id] += 1

        bee_data = np.concat([np.reshape([idx for idx in range(count)], (count, 1)), np.zeros([count, 3])], axis=1)

        self.bee_data = pd.DataFrame(
            data=bee_data, columns=["bee_id", "age", "state", "activity_time"], dtype=pd.UInt16Dtype
        )

    def process_iteration(self):
        self.bee_data["age"] += 1

        for bee in self.bees:
            changed_id = bee.process_iteration()
            if changed_id:
                # print(f"Changed ID: {changed_id}")
                self.activity_counts[changed_id[0]] -= 1
                self.activity_counts[changed_id[1]] += 1


if __name__ == "__main__":
    beehive = Beehive(count=10)
    beehive.process_iteration()

    print(beehive.bee_data)
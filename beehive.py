import datetime
import os.path
import random
import time
import numpy as np

from bee import BeeMachine
from beehive_display import BeehiveDisplay
from utils import *
import pandas as pd

rng = np.random.default_rng()


class Beehive:

    def __init__(self, count=5, start_state=None, display_size=(800, 600), load_from_save=True, restrict_speed=True):
        self.bee_data = None
        self.activity_counts = {i: 0 for i in BeeStates}

        if load_from_save:
            if os.path.exists("data/bee_states.csv"):
                self.bee_data = pd.read_csv(
                    "data/bee_states.csv",
                    index_col=0
                )

                state_counts = self.bee_data.value_counts(["state"]).to_dict()
                for k, v in state_counts.items():
                    self.activity_counts[BeeStates(k[0])] = v

                print(self.activity_counts)

            else:
                print("Load from file failed, initiating instead")
                self.initiate_bees(count)
        else:
            self.initiate_bees(count)

        self.bee_machines = [BeeMachine(bee_id=idx, start_state=BeeStates(bee_state)) for idx, bee_state in
                             enumerate(self.bee_data["state"].to_numpy())]

        self.display = BeehiveDisplay(display_size, count)

        self.running = False

        self.iter_count = 0
        self.iter_times = np.empty(1000, dtype=float)
        self.restrict_speed = restrict_speed

    def initiate_bees(self, count):
        bee_data = np.concat([
            np.reshape([idx for idx in range(count)], (count, 1)),
            np.zeros([count, 3]),
            np.reshape(np.repeat(20, count), (count, 1)),
        ], axis=1)

        self.bee_data = pd.DataFrame(
            data=bee_data, columns=["bee_id", "age", "state", "activity_time", "mean_activity_time"],
            dtype=pd.UInt16Dtype()
        )

        self.bee_data["state"] = BeeStates.initialise.birth

        self.bee_data = self.bee_data.set_index("bee_id")

        self.activity_counts[BeeStates.birth] = count


    def cycle_bee(self, bee_id, kill=False):
        if kill:
            self.bee_machines[bee_id].bee_death()

        res = self.bee_machines[bee_id].cycle()
        self.bee_data.loc[bee_id, ["state", "activity_time", "mean_activity_time"]] = [res[1].value, 0, activity_times[res[1]]]

        self.activity_counts[res[0]] -= 1
        self.activity_counts[res[1]] += 1

        self.display.add_new_transition(res[0], res[1])

    def process_iteration(self, visualise_transitions=True):
        t1 = time.monotonic()
        transition_ids = self.bee_data[self.bee_data.activity_time > 0.6 * self.bee_data.mean_activity_time].index
        if not transition_ids.empty:
            transition_ids = transition_ids[np.any(rng.random((1, len(transition_ids))) > 0.3, axis=0)]
            for bee_id in transition_ids:
                self.cycle_bee(bee_id)

        self.bee_data["activity_time"] += 1
        self.bee_data["age"] += 1
        self.display.sprites.increment_age()

        self.iter_count += 1
        if self.iter_count < 1000:
            self.iter_times[self.iter_count] = time.monotonic() - t1
        elif self.iter_count == 1000:
            print(np.mean(self.iter_times))
        if self.iter_count % 50 == 0:
            print(self.iter_count, f"Iteration time: {time.monotonic() - t1}")

        if visualise_transitions:
            self.display.render_hive(self.activity_counts)
            window.blit(self.display.get_surface(), (0, 0))
            pg.display.flip()
            pg.event.pump()



    def save_state(self):
        self.bee_data.to_csv(
            f"data/bee_states.csv"
        )

        state_counts = self.bee_data.value_counts(["state"]).to_dict()
        for k, v in state_counts.items():
            self.activity_counts[BeeStates(k[0])] = v

        print(self.activity_counts)

    def run(self):
        self.running = True

        window.blit(self.display.get_surface(), (0, 0))
        pg.display.flip()

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.save_state()

            self.display.refresh()
            t1 = time.monotonic()
            self.process_iteration(visualise_transitions=False)
            # print(beehive.activity_counts)
            if self.restrict_speed:
                while time.monotonic() - t1 < 0.1:
                    pass


if __name__ == "__main__":
    print(f"Creating beehive")

    pg.init()
    window = pg.display.set_mode((1200, 800))
    beehive = Beehive(10000, display_size=window.get_size(), load_from_save=False, restrict_speed=False)
    beehive.run()

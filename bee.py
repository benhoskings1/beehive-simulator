import random
from utils import *
import time

from statemachine import StateMachine, State


class Bee:
    def __init__(self, state=None):
        if state:
            self.activity_id = state
        else:
            self.activity_id = random.choice(list(activity_cycle.keys()))

        self.activity_prev = None
        self.activity_time = 0
        self.age = 0

    def process_iteration(self):
        changed = False
        pre_activity = self.activity_id
        if self.activity_time + random.randint(-5, 5) > activity_times[activity_cycle[self.activity_id]]:
            self.activity_id = (self.activity_id + 1) % len(activity_cycle)
            self.activity_time = 0
            changed = True

        self.activity_time += 1
        self.age += 1

        if changed:
            # self.print_status()
            return pre_activity, self.activity_id

    def print_status(self):
        print(f"Old Activity: {activity_cycle[self.activity_id]} (ID {(self.activity_id - 1) % len(activity_cycle)})\n"
              f"New Activity: {activity_cycle[self.activity_id]} (ID {self.activity_id})\n"
              f"Time: {self.activity_time}")


class BeeMachine(StateMachine):
    sleeping = State(initial=True, name="Sleeping", value=0)
    flying = State(name="Flying", value=1)
    gathering = State(name="Gathering", value=2)
    unloading = State(name="Unloading", value=3)
    dead = State(final=True, name="Dead", value=4)

    cycle = (
        sleeping.to(flying)
        | flying.to(gathering)
        | gathering.to(unloading)
        | unloading.to(sleeping)
    )

    bee_death = (
        sleeping.to(dead)
        | flying.to(dead)
        | gathering.to(dead)
        | unloading.to(dead)
    )

    def __init__(self):
        self.age = 0
        self.activity_time = 0
        super(BeeMachine, self).__init__()

    def before_cycle(self, event: str, source: State, target: State, message: str = ""):
        message = ". " + message if message else ""
        return f"Running {event} from {source.id} to {target.id}{message}"

    def after_cycle(self):
        self.age += 1

    def on_enter_dead(self):
        print("The bee died")


if __name__ == "__main__":
    bm = BeeMachine()

    for i in range(5):
        bm.cycle()

    bm.send("bee_death")
    print(bm.age)


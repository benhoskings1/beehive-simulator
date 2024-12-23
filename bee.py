import random
from utils import *
import time

from enum import Enum
from statemachine import StateMachine, State
from statemachine.states import States


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

    states = States.from_enum(
        BeeStates,
        initial=BeeStates.birth,
        final=BeeStates.dead,
        use_enum_instance=True,
    )

    # sleeping = State(initial=True, name="Sleeping", value=0)
    # flying = State(name="Flying", value=1)
    # gathering = State(name="Gathering", value=2)
    # unloading = State(name="Unloading", value=3)
    # dead = State(final=True, name="Dead", value=4)

    cycle = (
        states.birth.to(states.flying)
        | states.sleeping.to(states.flying)
        | states.flying.to(states.gathering, cond="gathering_transition")
        | states.gathering.to(states.flying)
        | states.flying.to(states.unloading)
        | states.unloading.to(states.sleeping)
    )

    bee_death = (
        states.sleeping.to(states.dead, )
        | states.flying.to(states.dead)
        | states.gathering.to(states.dead)
        | states.unloading.to(states.dead)
    )

    def __init__(self, bee_id):
        self.bee_id = bee_id
        self.prev_state = None
        super(BeeMachine, self).__init__()

    def before_cycle(self, source: State, target: State):
        self.prev_state = source
        # print(f"Cycling Bee: {self.bee_id} from {source.id} to {target.id}")
        return source.value, target.value

    def gathering_transition(self):
        return self.prev_state.value is not BeeStates.gathering

    def before_dead(self, target: State):
        return target.value.value

    def on_enter_dead(self):
        print("The bee died")


if __name__ == "__main__":
    bm = BeeMachine(bee_id=101)

    for i in range(5):
        print(bm.cycle())

    bm.send("bee_death")


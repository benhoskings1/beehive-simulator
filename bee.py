import random
from utils import *
import time

from enum import Enum
from statemachine import StateMachine, State
from statemachine.states import States


class BeeMachine(StateMachine):

    states = States.from_enum(
        BeeStates,
        initial=BeeStates.initialise,
        final=BeeStates.dead,
        use_enum_instance=True,
    )

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

    # dead = 0
    # birth = 1
    # sleeping = 2
    # flying = 3
    # gathering = 4
    # unloading = 5

    initialise = (
        states.initialise.to(states.dead, cond="initialise_transition") |
        states.initialise.to(states.birth, cond="initialise_transition") |
        states.initialise.to(states.sleeping, cond="initialise_transition") |
        states.initialise.to(states.flying, cond="initialise_transition") |
        states.initialise.to(states.gathering, cond="initialise_transition") |
        states.initialise.to(states.unloading, cond="initialise_transition")
    )

    def __init__(self, bee_id, start_state=BeeStates.birth):
        self.bee_id = bee_id
        self.prev_state = None
        self.idx_holder = 0
        super(BeeMachine, self).__init__()
        self.initialise(start_state)
        self.prev_state = start_state
        # print(self.current_state)

    def before_cycle(self, source: State, target: State):
        self.prev_state = source
        # print(f"Cycling Bee: {self.bee_id} from {source.id} to {target.id}")
        return source.value, target.value

    def initialise_transition(self, target_state):
        init_state = self.idx_holder == target_state.value
        if not init_state:
            self.idx_holder += 1
        return init_state

    def gathering_transition(self):
        return self.prev_state.value is not BeeStates.gathering

    def before_dead(self, target: State):
        return target.value.value

    def on_enter_dead(self):
        print("The bee died")


if __name__ == "__main__":
    bm = BeeMachine(bee_id=101, start_state=BeeStates.birth)
    img_path = "docs/images/readme_bee_machine.png"
    bm._graph().write_png(img_path)

    for i in range(5):
        print(bm.cycle())

    bm.send("bee_death")


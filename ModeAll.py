import ModeArcade
import ModeSoftList
import random


def get(machine_list, soft_list):
    rand = random.randrange(2)
    if rand == 0:
        return ModeArcade.get(machine_list)
    else:
        return ModeSoftList.get(machine_list, soft_list)

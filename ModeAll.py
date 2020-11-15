import ModeArcade
import ModeSoftList
import random


def get(machine_count, machine_list, soft_list_count, soft_list):
    rand = random.randrange(2)
    if rand == 0:
        return ModeArcade.get(machine_count, machine_list)
    else:
        return ModeSoftList.get(soft_list_count, machine_list, soft_list)

import random
import re

import MachineFilter
import Config

found_machine_list = []


def get(machine_list):
    if len(found_machine_list) == 0:
        generate_list(machine_list)

    rand = random.randrange(len(found_machine_list))
    command, description = found_machine_list[rand]
    found_machine_list.pop(rand)

    return command, description


def generate_list(machine_list):
    for machine in machine_list:

        machine, description = MachineFilter.get(machine)
        if machine is None:
            continue

        if Config.description is not None:
            if re.match(Config.description, description, re.IGNORECASE) is None:
                continue

        machine_input = machine.find("input")
        if machine_input is not None:
            if "coins" not in machine_input.attrib:
                # print("Skip non arcade machine ", machine.attrib['name'], "-", title)
                continue
        else:
            # print("Skip no input machine ", machine.attrib['name'], "-", title)
            continue

        found_machine_list.append([machine.attrib["name"], description])

    print("Arcade machines found :", len(found_machine_list))

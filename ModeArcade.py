import random

import MachineFilter


def get(machine_list):
    while True:
        rand = random.randrange(len(machine_list))
        machine = machine_list[rand]

        machine = MachineFilter.get(machine)
        if machine is None:
            continue

        description = machine.find("description")
        year = machine.find("year")

        full_name = "\"" + machine.attrib["name"] + "\"" + " - " + description.text + " - (" + year.text + ")"

        machine_input = machine.find("input")
        if machine_input is not None:
            if "coins" in machine_input.attrib:
                print("Run", full_name)
            else:
                print("Skip non arcade machine ", full_name)
                continue
        else:
            print("Skip no input machine ", full_name)
            continue

        return machine.attrib["name"]

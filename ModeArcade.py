import random

import MachineFilter


def get(machine_list):
    while True:
        rand = random.randrange(len(machine_list))
        machine = machine_list[rand]

        machine, title = MachineFilter.get(machine)
        if machine is None:
            continue

        machine_input = machine.find("input")
        if machine_input is not None:
            if "coins" in machine_input.attrib:
                print("Run", machine.attrib['name'], "-", title)
            else:
                print("Skip non arcade machine ", machine.attrib['name'], "-", title)
                continue
        else:
            print("Skip no input machine ", machine.attrib['name'], "-", title)
            continue

        return machine.attrib["name"], title

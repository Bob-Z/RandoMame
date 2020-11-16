import random
import ModeSelectedSoftList

import Config


def get(machine_list, soft_list):
    while True:
        rand = random.randrange(len(soft_list))
        selected_list = soft_list[rand]

        list_name = selected_list.attrib['name']

        command = ModeSelectedSoftList.get([list_name], machine_list, soft_list)

        if command is None:
            continue

        return command

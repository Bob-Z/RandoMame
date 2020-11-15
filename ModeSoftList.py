import random
import ModeSelectedSoftList

import Config


def get(soft_list_count, machine_list, soft_list):
    while True:
        rand = random.randrange(soft_list_count)
        selected_list = soft_list[rand]

        list_name = selected_list.attrib['name']

        command = ModeSelectedSoftList.get([list_name], machine_list, soft_list)

        if command is None:
            continue

        return command

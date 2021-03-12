import random

import CommandGeneratorMachine
import Config

item_list = []
first_pass = True


def get(machine_list):
    global item_list
    global first_pass
    if len(item_list) == 0:

        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        item_list = CommandGeneratorMachine.generate_command_list(machine_list)
        print(len(item_list), "arcade machines found")

    if len(item_list) == 0:
        return None

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))
    selected_item = item_list[rand]
    item_list.pop(rand)

    return selected_item

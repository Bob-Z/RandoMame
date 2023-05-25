import random

import CommandGeneratorMachine
import Config
import time

item_list = []
first_pass = True


def get(all_machine_xml):
    global item_list
    global first_pass
    if len(item_list) == 0:

        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        item_list = CommandGeneratorMachine.generate_command_list(all_machine_xml)
        if Config.mode == "arcade":
            print(len(item_list), "arcade machines found")
        elif Config.mode == "standalone":
            print(len(item_list), "standalone machines found")
        else:
            print(len(item_list), "slot machines found")

        time.sleep(1.5)

        if len(item_list) == 0:
            return None

        item_list.sort(key=lambda x: x.get_sort_criteria(), reverse=Config.sort_reverse)

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))
    selected_item = item_list[rand]
    item_list.pop(rand)

    return selected_item

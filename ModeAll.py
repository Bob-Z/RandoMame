import random

import CommandGeneratorMachine
import CommandGeneratorSoftList
import Config
import Display

item_list = []
first_pass = True


def get(machine_list, soft_list_list):
    global item_list
    global first_pass

    if len(item_list) == 0:

        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        generate_full_command_list(machine_list, soft_list_list)
        if len(item_list) == 0:
            Config.allow_preliminary = True
            Config.allow_not_supported = True

            generate_full_command_list(machine_list, soft_list_list)

        if len(item_list) != 0:
            item_list.sort(key=lambda x: x.get_sort_criteria(), reverse=Config.sort_reverse)

    if len(item_list) == 0:
        return None

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))
    selected_item = item_list[rand]
    item_list.pop(rand)

    return selected_item


def generate_full_command_list(machine_list, soft_list_list):
    global item_list
    item_list = CommandGeneratorMachine.generate_command_list(machine_list)

    found_qty = len(item_list)
    Display.print_text("Found " + str(found_qty) + " softwares" + Config.get_allowed_string())

    for soft_list in soft_list_list.findall("softwarelist"):
        new_item_list = CommandGeneratorSoftList.generate_command_list(machine_list, soft_list_list,
                                                                       soft_list.attrib['name'])

        if new_item_list is not None:
            item_list = item_list + new_item_list

        if len(item_list) > found_qty + 1000:
            found_qty = len(item_list)
            Display.print_text("Found " + str(found_qty) + " softwares" + Config.get_allowed_string())

    print(len(item_list), "machines or softwares found" + Config.get_allowed_string())

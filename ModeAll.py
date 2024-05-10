import random
import datetime

import CommandGeneratorMachine
import CommandGeneratorSoftList
import Config
import Display
import time

item_list = []
first_pass = True


def get(machine_list, soft_list_list, home_only=False):
    global item_list
    global first_pass

    if len(item_list) == 0:

        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        generate_full_command_list(machine_list, soft_list_list, home_only)
        if len(item_list) == 0:
            Config.allow_preliminary = True
            Config.allow_not_supported = True

            generate_full_command_list(machine_list, soft_list_list, home_only)

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


def generate_full_command_list(all_machine_xml, soft_list_list, home_only=False):
    global item_list

    if home_only is False:
        item_list = CommandGeneratorMachine.generate_command_list(all_machine_xml)

        found_qty = len(item_list)
        Display.print_text("Found " + str(found_qty) + " machines" + Config.get_allowed_string())

    softlist_qty = 0
    total_soft_with_compatible_machine_qty = 0
    total_soft_without_compatible_machine_qty = 0

    display_time = datetime.datetime.now()

    for soft_list in soft_list_list.findall("softwarelist"):
        new_item_list, soft_with_compatible_machine_qty, soft_without_compatible_machine_qty = CommandGeneratorSoftList.generate_command_list(
            all_machine_xml, soft_list_list,
            soft_list.attrib['name'])

        if new_item_list is not None:
            item_list = item_list + new_item_list

            total_soft_with_compatible_machine_qty = total_soft_with_compatible_machine_qty + soft_with_compatible_machine_qty
            total_soft_without_compatible_machine_qty = total_soft_without_compatible_machine_qty + soft_without_compatible_machine_qty

        found_qty = len(item_list)

        softlist_qty = softlist_qty + 1

        if datetime.datetime.now() >= display_time:
            if Config.windows_quantity > 0:
                Display.print_text_array(None, ["Found " + str(
                    found_qty) + " software " + Config.get_allowed_string(), "       " + str(softlist_qty) + "/" + str(
                    len(soft_list_list)) + " software lists analyzed         ",
                                                str(total_soft_with_compatible_machine_qty) + " have compatible machine"],
                                         True)
            display_time = datetime.datetime.now() + datetime.timedelta(seconds=0.5)

    time.sleep(1.5)

    (len(item_list), "machines or software found" + Config.get_allowed_string())

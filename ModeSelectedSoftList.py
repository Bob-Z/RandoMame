import random
import time

import CommandGeneratorSoftList
import Config
import Display

item_list = []
first_pass = True


def get(machine_xml_list, softlist_xml_list, softlist_name_list):
    global item_list
    global first_pass
    if len(item_list) == 0:
        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        generate_full_command_list(machine_xml_list, softlist_xml_list, softlist_name_list)

        if len(item_list) == 0:
            Config.allow_all()

            generate_full_command_list(machine_xml_list, softlist_xml_list, softlist_name_list)

    if len(item_list) == 0:
        return None

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))

    selected_item = item_list[rand]
    item_list.pop(rand)

    return selected_item


def generate_full_command_list(machine_xml_list, softlist_xml_list, softlist_name_list):
    global item_list

    for softlist_name in softlist_name_list:
        new_item_list = CommandGeneratorSoftList.generate_command_list(machine_xml_list, softlist_xml_list,
                                                                       softlist_name)
        if new_item_list is not None:
            item_list = item_list + new_item_list

        Display.print_text("Found " + str(len(item_list)) + " softwares" + Config.get_allowed_string())
        time.sleep(1.5)

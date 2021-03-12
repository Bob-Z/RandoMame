import random

import CommandGeneratorSoftList
import Config
import Display

item_list = []
first_pass = True


def get(machine_xml_list, softlist_xml_list):
    global item_list
    global first_pass
    if len(item_list) == 0:
        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        for softlist_xml in softlist_xml_list.findall("softwarelist"):
            new_item_list = CommandGeneratorSoftList.generate_command_list(machine_xml_list, softlist_xml_list,
                                                                           softlist_xml.attrib['name'])
            if new_item_list is not None:
                item_list = item_list + new_item_list

            Display.print_text("Found " + str(len(item_list)) + " softwares")

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))

    selected_item = item_list[rand]
    item_list.pop(rand)

    return selected_item

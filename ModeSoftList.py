import random

import CommandGeneratorSoftList
import Config
import Display
import time

item_list = []
first_pass = True


def get(machine_xml_list, softlist_xml_list):
    global item_list
    global first_pass
    if len(item_list) == 0:
        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        total_soft_with_compatible_machine_qty = 0
        total_soft_without_compatible_machine_qty = 0

        for softlist_xml in softlist_xml_list.findall("softwarelist"):
            new_item_list, soft_with_compatible_machine_qty, soft_without_compatible_machine_qty = CommandGeneratorSoftList.generate_command_list(
                machine_xml_list, softlist_xml_list,
                softlist_xml.attrib['name'])
            if new_item_list is not None:
                item_list = item_list + new_item_list

                total_soft_with_compatible_machine_qty = total_soft_with_compatible_machine_qty + soft_with_compatible_machine_qty
                total_soft_without_compatible_machine_qty = total_soft_without_compatible_machine_qty + soft_without_compatible_machine_qty

            Display.print_text_array(None, ["Found " + str(len(item_list)) + " software" + Config.get_allowed_string(),
                                            str(total_soft_with_compatible_machine_qty) + " have compatible machine"],
                                     True)

        if len(item_list) != 0:
            item_list.sort(key=lambda x: x.get_sort_criteria(), reverse=Config.sort_reverse)

        time.sleep(1.5)

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))

    selected_item = item_list[rand]
    item_list.pop(rand)

    return selected_item

import random

import FilterMachine
import FilterSoftware
from Item import Item

machine_xml_by_soft_list = {}


def generate_command_list(machine_xml_list, softlist_xml_list, softlist_name):
    item_list = generate_item_list(softlist_name, softlist_xml_list)

    if item_list is not None:
        for item in item_list:
            random_machine_item = pick_random_machine(machine_xml_list, item)
            if random_machine_item is None:
                # TODO do not return None for the whole list when only one item has no machine
                return None

            item.set_machine_xml(random_machine_item.get_machine_xml())

    return item_list


def generate_item_list(softlist_name, softlist_xml_list):
    found_software = []

    if softlist_name == "vgmplay":
        print("Skip vgmplay softlist")
        return None

    selected_softlist_xml = None

    for softlist_xml in softlist_xml_list.findall('softwarelist'):
        if softlist_xml.attrib['name'] == softlist_name:
            selected_softlist_xml = softlist_xml
            break

    if selected_softlist_xml is None:
        print("No software list named", softlist_name)
        return None

    for soft_xml in selected_softlist_xml:
        item = FilterSoftware.get(soft_xml)
        if item is None:
            continue

        item.set_softlist_name(softlist_name)

        found_software.append(item)

    if len(found_software) > 0:
        print("Found", len(found_software), "softwares in software list", softlist_name)

    return found_software


def pick_random_machine(machine_list, item):
    global machine_xml_by_soft_list

    if item.get_softlist_name() not in machine_xml_by_soft_list:
        machine_xml_by_soft_list[item.get_softlist_name()] = generate_machine_xml_list_for_soft_list(machine_list, item)

    # this can happen when this method is called more than one time since we pop out some elem
    if len(machine_xml_by_soft_list[item.get_softlist_name()]) == 0:
        machine_xml_by_soft_list[item.get_softlist_name()] = generate_machine_xml_list_for_soft_list(machine_list, item)

    found_machine_xml_list = machine_xml_by_soft_list[item.get_softlist_name()]

    machine_item = None

    while len(found_machine_xml_list) > 0:
        rand = random.randrange(len(found_machine_xml_list))

        machine_xml = found_machine_xml_list[rand]

        machine_item = FilterMachine.get(machine_xml, check_machine_description=False)

        if machine_item is None:
            found_machine_xml_list.pop(rand)
        else:
            break

    if machine_item is None:
        print("No machine available for software list", item.get_softlist_name())
        return None

    return machine_item


def generate_machine_xml_list_for_soft_list(machine_xml_list, item):
    found_machine_xml_list = []
    for machine_xml in machine_xml_list:
        machine_xml_softlist_list = machine_xml.findall("softwarelist")
        for machine_xml_softlist in machine_xml_softlist_list:
            if machine_xml_softlist.attrib['name'] == item.get_softlist_name():
                # This machine support selected soft_list

                temp_item = Item()
                temp_item.set_machine_xml(machine_xml)
                temp_item.set_soft_xml(item.get_soft_xml())
                interface_command_line = temp_item.get_interface_command_line()
                if interface_command_line != "":
                    # This machine has the correct interface for this software
                    found_machine_xml_list.append(machine_xml)
                    break

    return found_machine_xml_list

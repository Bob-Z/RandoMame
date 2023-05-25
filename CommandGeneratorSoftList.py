import random

import Config
import FilterMachine
import FilterSoftware
from Item import Item

machine_xml_by_soft_list = {}


def generate_command_list(all_machine_xml, softlist_xml_list, softlist_name):
    item_list = generate_item_list(all_machine_xml, softlist_name, softlist_xml_list)

    soft_with_compatible_machine_qty = 0
    soft_without_compatible_machine_qty = 0

    if item_list is not None:
        for item in item_list:
            random_machine_item = pick_random_machine(all_machine_xml, item)
            if random_machine_item is not None:
                item.set_machine_xml(random_machine_item.get_machine_xml())
                soft_with_compatible_machine_qty = soft_with_compatible_machine_qty + 1
            else:
                item.set_machine_xml(None)
                soft_without_compatible_machine_qty = soft_without_compatible_machine_qty + 1

        # Remove item with empty machine_xml
        item_list = [item for item in item_list if item.get_machine_xml()]

    print(soft_with_compatible_machine_qty, "soft with machine")
    print(soft_without_compatible_machine_qty, "soft without machine")

    return item_list, soft_with_compatible_machine_qty, soft_without_compatible_machine_qty


def generate_item_list(all_machine_xml, softlist_name, softlist_xml_list):
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

    total_soft_qty = 0
    for soft_xml in selected_softlist_xml:
        total_soft_qty = total_soft_qty + 1
        item = FilterSoftware.get(all_machine_xml, soft_xml)
        if item is None:
            continue

        item.set_softlist_name(softlist_name)

        found_software.append(item)

    print(total_soft_qty, "software in", softlist_name)
    if len(found_software) > 0:
        print("Found", len(found_software), " of ", total_soft_qty, "software in", softlist_name, "software list")

    return found_software


def pick_random_machine(all_machine_xml, item):
    global machine_xml_by_soft_list

    if item.get_softlist_name() not in machine_xml_by_soft_list:
        if Config.force_driver is None:
            machine_xml_by_soft_list[item.get_softlist_name()] = generate_machine_xml_list_for_soft_list(
                all_machine_xml,
                item)
        else:
            machine_xml_by_soft_list[item.get_softlist_name()] = generate_machine_xml_list_from_forced_driver(
                all_machine_xml)

    found_machine_xml_list = list(machine_xml_by_soft_list[item.get_softlist_name()])

    machine_item = None

    while len(found_machine_xml_list) > 0:
        rand = random.randrange(len(found_machine_xml_list))

        machine_xml = found_machine_xml_list[rand]

        machine_item = FilterMachine.get(all_machine_xml, machine_xml, False, item)

        if machine_item is None:
            found_machine_xml_list.pop(rand)
        else:
            break

    return machine_item


def generate_machine_xml_list_for_soft_list(all_machine_xml, item):
    found_machine_xml_list = []
    is_parent_first = Config.prefer_parent

    while True:
        for machine_xml in all_machine_xml:
            if is_parent_first is True:
                if 'cloneof' in machine_xml.attrib:
                    continue

            machine_xml_softlist_list = machine_xml.findall("softwarelist")
            for machine_xml_softlist in machine_xml_softlist_list:
                if machine_xml_softlist.attrib['name'] == item.get_softlist_name():
                    # This machine support selected soft_list
                    temp_item = Item(all_machine_xml)
                    temp_item.set_machine_xml(machine_xml)
                    temp_item.set_soft_xml(item.get_soft_xml())
                    interface_command_line = temp_item.get_interface_command_line()
                    if interface_command_line != "":
                        # This machine has the correct interface for this software
                        found_machine_xml_list.append(machine_xml)

        if is_parent_first is False:
            return found_machine_xml_list

        is_parent_first = False


def generate_machine_xml_list_from_forced_driver(machine_xml_list):
    found_machine_xml_list = []

    for machine_xml in machine_xml_list:
        for d in Config.force_driver:
            if machine_xml.attrib['name'] == d:
                found_machine_xml_list.append(machine_xml)
                break

    return found_machine_xml_list

import configparser
import re

import Config
import Display
from Item import Item

ini_data = None


def get(machine_xml, check_machine_description):
    global ini_data
    if Config.ini_file is not None:
        if ini_data is None:
            ini_data = configparser.ConfigParser(allow_no_value=True)
            ini_data.read(Config.ini_file)

    if Config.force_driver is not None:
        found = False
        drivers = Config.force_driver.split(',')
        for d in drivers:
            if machine_xml.attrib['name'] == d:
                found = True

        if found is False:
            return None

    if "isdevice" in machine_xml.attrib:
        if machine_xml.attrib["isdevice"] == "yes":
            # print("Skip device ", machine.attrib["name"])
            return None
    if "isbios" in machine_xml.attrib:
        if machine_xml.attrib["isbios"] == "yes":
            # print("Skip bios ", machine.attrib["name"])
            return None
    if "runnable" in machine_xml.attrib:
        if machine_xml.attrib["runnable"] == "no":
            # print("Skip non runnable ", machine.attrib["name"])
            return None
    #if "ismechanical" in machine.attrib:
    #    if machine.attrib["ismechanical"] == "yes":
            # print("Skip mechanical ", machine.attrib["name"])
    #        return None

    if Config.allow_preliminary is False:
        machine_driver = machine_xml.find("driver")
        if machine_driver is not None:
            if "status" in machine_driver.attrib:
                if machine_driver.attrib["status"] == "preliminary":
                    # print("Skip preliminary driver machine ", machine.attrib["name"])
                    return None

    year = machine_xml.find("year").text
    if Config.year_min is not None:
        try:
            if int(year) < Config.year_min:
                return None
        except ValueError:
            return None

    if Config.year_max is not None:
        try:
            if int(year) > Config.year_max:
                return None
        except ValueError:
            return None

    if Config.description is not None and check_machine_description is True:
        if strict_search_machine(machine_xml) is False:
            return None

    if Config.manufacturer is not None:
        current_manuf = machine_xml.find("manufacturer").text
        manuf_list = Config.manufacturer.split(',')
        is_found = False
        for manuf in manuf_list:
            if re.match(manuf, current_manuf, re.IGNORECASE) is not None:
                is_found = True
                break

        if is_found is False:
            return None

    if Config.ini_file is not None:
        if Config.include is not None:
            found = False
            for i in Config.include.split(','):
                if machine_xml.attrib['name'] in ini_data[i]:
                    found = True
                    break
            if found is False:
                return None
        if Config.exclude is not None:
            try:
                for e in Config.exclude.split(','):
                    if machine_xml.attrib['name'] in ini_data[e]:
                        return None
            except KeyError:
                pass

    if Config.source_file is not None:
        source_file_list = Config.source_file.split(',')
        is_found = False
        for source_file in source_file_list:
            if machine_xml.attrib['sourcefile'] == source_file:
                is_found = True
                break
        if is_found is False:
            return None

    if Config.no_clone is True and "cloneof" in machine_xml.attrib:
        return None

    if Config.device is not None:
        is_found = False
        machine_device = machine_xml.findall("device_ref")
        if machine_device is not None:
            for md in machine_device:
                for d in Config.device.split(','):
                    if md.attrib["name"] == d:
                        is_found = True
                        break

                if is_found is True:
                    break;

        if is_found is False:
            return None

    if Config.mode == 'arcade':
        machine_input = machine_xml.find("input")
        if machine_input is not None:
            if "coins" not in machine_input.attrib:
                # print("Skip non arcade machine ", machine.attrib['name'], "-", title)
                return None
        else:
            # print("Skip no input machine ", machine.attrib['name'], "-", title)
            return None

    item = Item()

    item.set_machine_xml(machine_xml)

    return item


def loose_search_machine_list(machine_list):
    new_machine_list = []

    for desc in Config.description:
        found_qty = 2

        for machine in machine_list:
            if exact_search_machine(machine, desc) is True:
                found_machine = machine
                found_qty = 1
                break

        # Trying to find a single machine matching the most word in Config.description
        desc_list = desc.split(' ')
        word_qty = 0

        while found_qty > 1:
            # Build a search string from words in Config.description starting from last word and adding the previous one by one.
            word_qty += 1

            if word_qty > len(desc_list):
                # Unable to find a single machine corresponding to all words in Config.description
                found_qty = 0
                break

            # s = ".*"
            s = ""
            for j in range(-word_qty, 0):
                s += desc_list[j]
                s += ' '

            # remove last ' '
            search_string = s[:-1]

            found_qty = 0

            for machine in machine_list:
                if loose_search_machine(machine, search_string) is True:
                    found_qty += 1
                    found_machine = machine
                    if found_qty > 1:
                        break

        if found_qty == 1:
            new_machine_list.append(found_machine)
            Display.print_text("Loose search find " + str(len(new_machine_list)) + " machines")
        else:
            print("No loose match for", search_string)

    return new_machine_list


def exact_search_machine(machine, search_string):
    description = machine.find("description").text
    s = "^" + search_string + "$"
    if re.search(s, description, re.IGNORECASE) is not None:
        return True

    return False


def loose_search_machine(machine, search_string):
    description = machine.find("description").text
    s = ".*" + search_string
    if re.search(s, description, re.IGNORECASE) is not None:
        return True

    return False


def strict_search_machine(machine):
    description = machine.find("description").text
    for desc in Config.description:
        if re.match(desc, description, re.IGNORECASE) is not None:
            return True

    return False

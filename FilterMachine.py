import re
import configparser

import Config
import Display
import unicodedata

ini_data = None


def get(machine, check_machine_description):
    global ini_data
    if Config.ini_file is not None:
        if ini_data is None:
            ini_data = configparser.ConfigParser(allow_no_value=True)
            ini_data.read(Config.ini_file)

    if "isdevice" in machine.attrib:
        if machine.attrib["isdevice"] == "yes":
            # print("Skip device ", machine.attrib["name"])
            return None, None
    if "isbios" in machine.attrib:
        if machine.attrib["isbios"] == "yes":
            # print("Skip bios ", machine.attrib["name"])
            return None, None
    if "runnable" in machine.attrib:
        if machine.attrib["runnable"] == "no":
            # print("Skip non runnable ", machine.attrib["name"])
            return None, None
    if "ismechanical" in machine.attrib:
        if machine.attrib["ismechanical"] == "yes":
            # print("Skip mechanical ", machine.attrib["name"])
            return None, None

    if Config.allow_preliminary is False:
        machine_driver = machine.find("driver")
        if machine_driver is not None:
            if "status" in machine_driver.attrib:
                if machine_driver.attrib["status"] == "preliminary":
                    # print("Skip preliminary driver machine ", machine.attrib["name"])
                    return None, None

    year = machine.find("year").text
    if Config.year_min is not None:
        try:
            if int(year) < Config.year_min:
                return None, None
        except ValueError:
            return None, None

    if Config.year_max is not None:
        try:
            if int(year) > Config.year_max:
                return None, None
        except ValueError:
            return None, None

    if Config.description is not None and check_machine_description is True:
        if strict_search_machine(machine) is False:
            return None, None

    if Config.manufacturer is not None:
        current_manuf = machine.find("manufacturer").text
        manuf_list = Config.manufacturer.split(',')
        is_found = False
        for manuf in manuf_list:
            if re.match(manuf, current_manuf, re.IGNORECASE) is not None:
                is_found = True
                break

        if is_found is False:
            return None, None

    if Config.ini_file is not None:
        if Config.include is not None:
            found = False
            for i in Config.include.split(','):
                if machine.attrib['name'] in ini_data[i]:
                    found = True
                    break
            if found is False:
                return None, None
        if Config.exclude is not None:
            try:
                for e in Config.exclude.split(','):
                    if machine.attrib['name'] in ini_data[e]:
                        return None, None
            except KeyError:
                pass

    if Config.mode == 'arcade':
        machine_input = machine.find("input")
        if machine_input is not None:
            if "coins" not in machine_input.attrib:
                # print("Skip non arcade machine ", machine.attrib['name'], "-", title)
                return None, None
        else:
            # print("Skip no input machine ", machine.attrib['name'], "-", title)
            return None, None

    description = machine.find("description").text
    full_name = description + " (" + year + ")"

    if 'cloneof' in machine.attrib:
        machine_list = [machine.attrib['name'], machine.attrib['cloneof']]
    else:
        machine_list = [machine.attrib['name']]
    return machine_list, full_name


def loose_search_machine_list(machine_list):
    new_machine_list = []
    for desc in Config.description:
        found_qty = 2
        word_qty = 0

        while found_qty > 1:
            word_qty += 1
            #s = ".*"
            s = ""
            desc_list = desc.split(' ')
            for j in range(-word_qty, 0):
                s += desc_list[j]
                s += ' '

            # remove last ' '
            search_string = s[:-1]

            found_qty = 0
            for machine in machine_list:
                if exact_search_machine(machine, search_string) is True:
                    found_machine = machine
                    found_qty = 1
                    break
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
    s = search_string+"$"
    if re.match(s, description, re.IGNORECASE) is not None:
        return True

    return False


def loose_search_machine(machine, search_string):
    description = machine.find("description").text
    s = ".*" + search_string
    if re.match(s, description, re.IGNORECASE) is not None:
        return True

    return False


def strict_search_machine(machine):
    description = machine.find("description").text
    for desc in Config.description:
        if re.match(desc, description, re.IGNORECASE) is not None:
            return True

    return False

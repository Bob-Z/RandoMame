import re

import Config


def get(machine, check_machine_description=True):
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

    description = machine.find("description").text
    if Config.description is not None and check_machine_description is True:
        for desc in Config.description:
            found = False
            if re.match(desc, description, re.IGNORECASE) is not None:
                found = True
                break

        if found is False:
            return None, None

    if Config.manufacturer is not None:
        current_manuf = machine.find("manufacturer").text
        manuf_list = Config.manufacturer.split(',')
        is_found = False
        for manuf in manuf_list:
            if current_manuf == manuf:
                is_found = True
                break

        if is_found is False:
            return None, None

    if Config.mode == 'arcade':
        machine_input = machine.find("input")
        if machine_input is not None:
            if "coins" not in machine_input.attrib:
                # print("Skip non arcade machine ", machine.attrib['name'], "-", title)
                return None, None
        else:
            # print("Skip no input machine ", machine.attrib['name'], "-", title)
            return None, None

    full_name = description + " (" + year + ")"

    return machine.attrib['name'], full_name

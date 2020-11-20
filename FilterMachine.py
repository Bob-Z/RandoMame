import Config


def get(machine):
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

    description = machine.find("description")
    if Config.description is not None:
        if re.match(Config.description, description, re.IGNORECASE) is None:
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

    full_name = description.text + " (" + year + ")"

    return machine.attrib['name'], full_name

import Config


def get(machine):
    if "isdevice" in machine.attrib:
        if machine.attrib["isdevice"] == "yes":
            print("Skip device ", machine.attrib["name"])
            return None, None
    if "isbios" in machine.attrib:
        if machine.attrib["isbios"] == "yes":
            print("Skip bios ", machine.attrib["name"])
            return None, None
    if "runnable" in machine.attrib:
        if machine.attrib["runnable"] == "no":
            print("Skip non runnable ", machine.attrib["name"])
            return None, None
    if "ismechanical" in machine.attrib:
        if machine.attrib["ismechanical"] == "yes":
            print("Skip mechanical ", machine.attrib["name"])
            return None, None

    if Config.allow_preliminary is False:
        machine_driver = machine.find("driver")
        if machine_driver is not None:
            if "status" in machine_driver.attrib:
                if machine_driver.attrib["status"] == "preliminary":
                    print("Skip preliminary driver machine ", machine.attrib["name"])
                    return None, None

    description = machine.find("description")
    year = machine.find("year")

    full_name = description.text + " (" + year.text + ")"

    return machine, full_name

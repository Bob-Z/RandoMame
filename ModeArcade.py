import random

import Config


def get(machine_count, machine_list):
    while True:
        rand = random.randrange(machine_count)
        machine = machine_list[rand]

        if "isdevice" in machine.attrib:
            if machine.attrib["isdevice"] == "yes":
                print("Skip device ", machine.attrib["name"])
                continue
        if "isbios" in machine.attrib:
            if machine.attrib["isbios"] == "yes":
                print("Skip bios ", machine.attrib["name"])
                continue
        if "runnable" in machine.attrib:
            if machine.attrib["runnable"] == "no":
                print("Skip non runnable ", machine.attrib["name"])
                continue
        if "ismechanical" in machine.attrib:
            if machine.attrib["ismechanical"] == "yes":
                print("Skip mechanical ", machine.attrib["name"])
                continue

        description = machine.find("description")
        year = machine.find("year")

        full_name = "\"" + machine.attrib["name"] + "\"" + " - " + description.text + " - (" + year.text + ")"

        if Config.allow_preliminary is False:
            machine_driver = machine.find("driver")
            if machine_driver is not None:
                if "status" in machine_driver.attrib:
                    if machine_driver.attrib["status"] == "preliminary":
                        print("Skip preliminary driver machine ", full_name)
                        continue

        machine_input = machine.find("input")
        if machine_input is not None:
            if "coins" in machine_input.attrib:
                print("Run", full_name)
            else:
                print("Skip non arcade machine ", full_name)
                continue
        else:
            print("Skip no input machine ", full_name)
            continue

        return machine.attrib["name"]

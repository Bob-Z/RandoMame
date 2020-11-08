import random


def get(machine_count, root):
    while True:
        rand = random.randrange(machine_count)
        machine = root[rand]

        if machine.attrib["isdevice"] == "yes":
            print("Skip device ", machine.attrib["name"])
            continue
        if machine.attrib["runnable"] == "no":
            print("Skip non runnable ", machine.attrib["name"])
            continue
        if machine.attrib["ismechanical"] == "yes":
            print("Skip mechanical ", machine.attrib["name"])
            continue

        description = machine.find("description")
        year = machine.find("year")

        full_name = "\"" + machine.attrib["name"] + "\"" + " - " + description.text + " - (" + year.text + ")"

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

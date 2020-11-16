import random

import Config


def get(selected_softlist, machine_list, soft_list):
    while True:
        if len(selected_softlist) == 0:
            if Config.mode == "selected_softlist":
                print("No valid softlist found")
                exit(1)
            else:
                return None

        rand = random.randrange(len(selected_softlist))
        list_name = selected_softlist[rand]

        selected_list = None
        for s in soft_list.findall('softwarelist'):
            if s.attrib['name'] == list_name:
                selected_list = s

        if selected_list is None:
            print("Can't find softlist", list_name)
            selected_softlist.pop(rand)
            continue

        machine_name = find_machine(machine_list, list_name)
        if machine_name is None:
            selected_softlist.pop(rand)
            continue

        software_command = find_software(list_name, selected_list)

        command = machine_name + " " + software_command

        return command


def find_machine(machine_list, list_name):
    print("Searching a machine for software list", list_name)

    found_machine = []
    for machine in machine_list:
        all_machine_soft_list = machine.findall("softwarelist")
        for machine_soft_list in all_machine_soft_list:
            if machine_soft_list.attrib['name'] == list_name:
                found_machine.append(machine)

    print("Found", len(found_machine), " machines for softlist", list_name)

    while len(found_machine) > 0:
        rand = random.randrange(len(found_machine))

        machine = found_machine[rand]

        if "isdevice" in machine.attrib:
            if machine.attrib["isdevice"] == "yes":
                print("Skip device ", machine.attrib["name"])
                found_machine.pop(rand)
                continue
        if "isbios" in machine.attrib:
            if machine.attrib["isbios"] == "yes":
                print("Skip bios ", machine.attrib["name"])
                found_machine.pop(rand)
                continue
        if "runnable" in machine.attrib:
            if machine.attrib["runnable"] == "no":
                print("Skip non runnable ", machine.attrib["name"])
                found_machine.pop(rand)
                continue
        if "ismechanical" in machine.attrib:
            if machine.attrib["ismechanical"] == "yes":
                print("Skip mechanical ", machine.attrib["name"])
                found_machine.pop(rand)
                continue

        if Config.allow_preliminary is False:
            machine_driver = machine.find("driver")
            if machine_driver is not None:
                if "status" in machine_driver.attrib:
                    if machine_driver.attrib["status"] == "preliminary":
                        print("Skip preliminary driver machine ", machine.attrib["name"])
                        found_machine.pop(rand)
                        continue
        description = machine.find("description")
        year = machine.find("year")
        full_name = "\"" + machine.attrib["name"] + "\"" + " - " + description.text + " - (" + year.text + ")"

        break

    if len(found_machine) == 0:
        print("No machine available for software  list", list_name)
        return None

    print("Using machine", full_name)

    return machine.attrib["name"]


def find_software(list_name, selected_list):
    software_count = 0
    for s in selected_list.findall('software'):
        software_count += 1

    print(software_count, "softwares in list", list_name)

    rand = random.randrange(software_count)
    selected_software = selected_list[rand]
    software_description = selected_software.find('description')
    software_name = selected_software.attrib['name']

    print("Running software \"", software_name, "\": ", software_description.text)

    software_command = software_name

    return software_command

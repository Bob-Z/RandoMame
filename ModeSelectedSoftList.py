import random

import Config
import MachineFilter


def get(user_softlist, machine_list, soft_list):
    while True:
        if len(user_softlist) == 0:
            if Config.mode == "selected_softlist":
                print("No valid softlist found")
                exit(1)
            else:
                return None

        rand = random.randrange(len(user_softlist))
        list_name = user_softlist[rand]

        selected_list = None
        for s in soft_list.findall('softwarelist'):
            if s.attrib['name'] == list_name:
                selected_list = s

        if selected_list is None:
            print("Can't find softlist", list_name)
            user_softlist.pop(rand)
            continue

        machine_name, full_machine_name = find_machine(machine_list, list_name)
        if machine_name is None:
            user_softlist.pop(rand)
            continue

        software_command, full_software_name = find_software(list_name, selected_list)

        command = machine_name + " " + software_command
        title = full_software_name + " // " + full_machine_name

        return command, title


def find_machine(machine_list, list_name):
    print("Searching machines for software list", list_name)

    found_machine_list = []
    for machine in machine_list:
        all_machine_soft_list = machine.findall("softwarelist")
        for machine_soft_list in all_machine_soft_list:
            if machine_soft_list.attrib['name'] == list_name:
                found_machine_list.append(machine)

    print("Found", len(found_machine_list), "machines for softlist", list_name)

    while len(found_machine_list) > 0:
        rand = random.randrange(len(found_machine_list))

        machine = found_machine_list[rand]

        machine, title = MachineFilter.get(machine)

        if machine is None:
            found_machine_list.pop(rand)
            continue

        break

    if len(found_machine_list) == 0:
        print("No machine available for software  list", list_name)
        return None, None

    print("Select machine", machine.attrib['name'], "-", title)

    return machine.attrib["name"], title


def find_software(list_name, selected_softlist):
    print("Found", len(selected_softlist), "softwares in list", list_name)

    rand = random.randrange(len(selected_softlist))
    selected_software = selected_softlist[rand]
    software_description = selected_software.find('description')
    software_name = selected_software.attrib['name']
    year = selected_software.find("year").text

    print("Select software \"" + software_name + "\": ", software_description.text)

    title = software_description.text + " (" + year + ")"
    return software_name, title

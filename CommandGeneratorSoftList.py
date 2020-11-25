import random

import FilterMachine
import FilterSoftware

machine_by_soft_list = {}


def generate_command_list(machine_list, soft_list_list, soft_list_name):
    command_list = []
    soft_list = generate_soft_list(soft_list_name, soft_list_list)
    if soft_list is None:
        return command_list

    for soft in soft_list:
        machine_name, full_machine_name = find_machine(machine_list, soft['softlist_name'])
        if machine_name is None:
            continue

        command = machine_name + " " + soft['soft_name']
        title = soft['description'] + " // " + full_machine_name

        command_list.append([command, title])

    return command_list


def generate_soft_list(soft_list_name, soft_list_list):
    found_software = []

    if soft_list_name == "vgmplay":
        print("Skip vgmplay softlist")
        return None

    selected_soft_list = None
    for soft_list in soft_list_list.findall('softwarelist'):
        if soft_list.attrib['name'] == soft_list_name:
            selected_soft_list = soft_list
            break

    if selected_soft_list is None:
        print("No software list named", soft_list_name)
        return None

    for soft in selected_soft_list:
        soft_name, description = FilterSoftware.get(soft)
        if soft_name is None:
            continue

        found_software.append({'softlist_name': soft_list_name, 'soft_name': soft_name, 'description': description})

    if len(found_software) > 0:
        print("Found", len(found_software), "softwares in software list", soft_list_name)

    return found_software


def find_machine(machine_list, list_name):
    global machine_by_soft_list
    try:
        found_machine_list = machine_by_soft_list[list_name]
    except KeyError:
        found_machine_list = []
        for machine in machine_list:
            all_machine_soft_list = machine.findall("softwarelist")
            for machine_soft_list in all_machine_soft_list:
                if machine_soft_list.attrib['name'] == list_name:
                    found_machine_list.append(machine)
                    break

        machine_by_soft_list[list_name] = found_machine_list

    while len(found_machine_list) > 0:
        rand = random.randrange(len(found_machine_list))

        machine = found_machine_list[rand]

        machine_name, title = FilterMachine.get(machine, check_machine_description=False)

        if machine_name is None:
            found_machine_list.pop(rand)
            continue

        break

    if len(found_machine_list) == 0:
        print("No machine available for software  list", list_name)
        return None, None

    return machine_name, title
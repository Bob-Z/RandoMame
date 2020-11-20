import random
import re

import MachineFilter
import Config

generated_soft_list = []
found_software = []


def get(soft_list_name_list, machine_list, soft_list_list):
    global found_software
    for soft_list_name in soft_list_name_list:
        generate_list(soft_list_name, soft_list_list)

    rand = random.randrange(len(found_software))
    soft = found_software[rand]

    machine_name, full_machine_name = find_machine(machine_list, soft['softlist_name'])

    if machine_name is None:
        return None, None

    command = machine_name + " " + soft['soft_name']
    title = soft['description'] + " // " + full_machine_name

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


def generate_list(soft_list_name, soft_list_list):
    global generated_soft_list
    if soft_list_name in generated_soft_list:
        return

    generated_soft_list.append(soft_list_name)

    selected_soft_list = None
    for soft_list in soft_list_list.findall('softwarelist'):
        if soft_list.attrib['name'] == soft_list_name:
            selected_soft_list = soft_list
            break

    if selected_soft_list is None:
        print("No software list named", softlist_name)
        return

    for soft in selected_soft_list:
        soft_description = soft.find('description')

        if Config.description is not None:
            if re.match(Config.description, soft_description.text, re.IGNORECASE) is None:
                continue

        year = soft.find('year').text
        if Config.year_min is not None:
            try:
                if int(year) < Config.year_min:
                    continue
            except ValueError:
                continue

        if Config.year_max is not None:
            try:
                if int(year) > Config.year_max:
                    continue
            except ValueError:
                continue

        soft_name = soft.attrib['name']

        description = soft_description.text + " (" + year + ")"

        global found_software
        found_software.append({'softlist_name': soft_list_name, 'soft_name': soft_name, 'description': description})

    print("Found", len(found_software), "corresponding softwares in software list", soft_list_name)

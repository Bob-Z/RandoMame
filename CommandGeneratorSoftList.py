import random

import FilterMachine
import FilterSoftware
import AutoBoot

machine_by_soft_list = {}


def generate_command_list(machine_list, soft_list_list, soft_list_name):
    command_list = []
    soft_list = generate_soft_list(soft_list_name, soft_list_list)
    if soft_list is None:
        return command_list

    for soft in soft_list:
        machine, machine_name, full_machine_name = pick_random_machine(machine_list, soft['softlist_name'])
        if machine_name is None:
            continue

        interface_command_line = get_interface_command_line(machine, soft)
        command = machine_name[0] + " " + interface_command_line + " " + soft['soft_name']

        autoboot_script, autoboot_delay, extra_command = AutoBoot.get_autoboot_command(soft_list_name, machine_name[0])
        if autoboot_delay is not None:
            command = command + " -autoboot_script autoboot_script/" + autoboot_script + " -autoboot_delay " + str(
                autoboot_delay)

        if extra_command is not None:
            command = command + " " + extra_command

        command_list.append([command, full_machine_name, soft['description'], machine_name])

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

        part = soft.findall("part")
        soft_interface = part[0].attrib["interface"]

        found_software.append({'softlist_name': soft_list_name, 'soft_name': soft_name, 'description': description, 'interface': soft_interface})

    if len(found_software) > 0:
        print("Found", len(found_software), "softwares in software list", soft_list_name)

    return found_software


def pick_random_machine(machine_list, list_name):
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
        return None, None, None

    return machine, machine_name, title


def get_interface_command_line(machine, soft):
    device = machine.findall("device")
    command_line = ""
    for d in device:
        if 'interface' in d.attrib:
            if d.attrib['interface'] == soft.get("interface"):
                instance = d.find("instance")
                interface_name = instance.attrib["briefname"]
                command_line = "-" + interface_name
                break

    return command_line

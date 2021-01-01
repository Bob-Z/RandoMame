import FilterMachine
import Config


def generate_command_list(machine_list):
    command_list = []

    check_machine_description = True

    if Config.loose_search is True:
        machine_list = FilterMachine.loose_search_machine_list(machine_list)
        check_machine_description = False

    for machine in machine_list:
        command, machine_desc = FilterMachine.get(machine, check_machine_description)
        if command is None:
            continue

        command_list.append([command[0], machine_desc, None, command])

    return command_list

import FilterMachine


def generate_command_list(machine_list):
    command_list = []
    for machine in machine_list:

        command, machine_desc = FilterMachine.get(machine)
        if command is None:
            continue

        command_list.append([command, machine_desc, None])

    return command_list

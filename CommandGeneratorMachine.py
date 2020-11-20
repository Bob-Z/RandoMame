import FilterMachine


def generate_command_list(machine_list):
    command_list = []
    for machine in machine_list:

        machine_name, description = FilterMachine.get(machine)
        if machine_name is None:
            continue

        command_list.append([machine_name, description])

    return command_list

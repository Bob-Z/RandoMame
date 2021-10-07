import FilterMachine
import Config


def generate_command_list(machine_list):
    item_list = []

    check_machine_description = True

    if Config.loose_search is True:
        machine_list = FilterMachine.loose_search_machine_list(machine_list)
        check_machine_description = False

    for machine in machine_list:
        item = FilterMachine.get(machine, check_machine_description)
        if item is None:
            continue

        item_list.append(item)

    if Config.sort_by_name is True:
        item_list.sort(key=lambda x: x.get_machine_full_description(), reverse=Config.sort_reverse)

    if Config.sort_by_year is True:
        item_list.sort(key=lambda x: x.get_machine_year() + " " + x.get_machine_description(),
                       reverse=Config.sort_reverse)

    return item_list

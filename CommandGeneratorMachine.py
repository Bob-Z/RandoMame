import FilterMachine
import Config


def generate_command_list(all_machine_xml):
    item_list = []

    check_machine_description = True

    if Config.loose_search is True:
        all_machine_xml = FilterMachine.loose_search_machine_list(all_machine_xml)
        check_machine_description = False

    if Config.multi_search is True:
        all_machine_xml = FilterMachine.multi_search_machine_list(all_machine_xml)
        check_machine_description = False

    for machine in all_machine_xml:
        item = FilterMachine.get(all_machine_xml, machine, check_machine_description, None)
        if item is None:
            continue

        item_list.append(item)

    return item_list

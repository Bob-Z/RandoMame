import ModeSelectedSoftList


def get(machine_list, soft_list_list):
    all_soft_list_name = []

    for soft_list in soft_list_list.findall("softwarelist"):
        all_soft_list_name.append(soft_list.attrib['name'])

    while True:
        command, title = ModeSelectedSoftList.get(all_soft_list_name, machine_list, soft_list_list)
        if command is not None:
            return command, title

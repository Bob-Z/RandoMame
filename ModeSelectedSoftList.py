import random

import CommandGeneratorSoftList
import Config

command_list = []


def get(machine_list, soft_list_list, soft_list_name_list):
    global command_list
    if len(command_list) == 0:
        for soft_list_name in soft_list_name_list:
            command_list = command_list + CommandGeneratorSoftList.generate_command_list(machine_list, soft_list_list,
                                                                                         soft_list_name)
            print(len(command_list), "softwares found in list", soft_list_name)

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(command_list))

    command, description = command_list[rand]
    command_list.pop(rand)

    return command, description

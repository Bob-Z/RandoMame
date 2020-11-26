import random

import CommandGeneratorMachine
import CommandGeneratorSoftList
import Config

command_list = []


def get(machine_list, soft_list_list):
    global command_list
    if len(command_list) == 0:
        command_list = CommandGeneratorMachine.generate_command_list(machine_list)
        for soft_list in soft_list_list.findall("softwarelist"):
            command_list = command_list + CommandGeneratorSoftList.generate_command_list(machine_list, soft_list_list,
                                                                                         soft_list.attrib['name'])

        print(len(command_list), "machines or softwares found")

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(command_list))
    command, description = command_list[rand]
    command_list.pop(rand)

    return command, description

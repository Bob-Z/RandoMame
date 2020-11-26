import random

import CommandGeneratorMachine
import Config

command_list = []


def get(machine_list):
    global command_list
    if len(command_list) == 0:
        command_list = CommandGeneratorMachine.generate_command_list(machine_list)
        print(len(command_list), "arcade machines found")

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(command_list))
    command, description = command_list[rand]
    command_list.pop(rand)

    return command, description

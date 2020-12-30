import random

import CommandGeneratorMachine
import Config

command_list = []
first_pass = True


def get(machine_list):
    global command_list
    global first_pass
    if len(command_list) == 0:

        if first_pass is False and Config.auto_quit is True:
            return None, None, None, None
        first_pass = False

        command_list = CommandGeneratorMachine.generate_command_list(machine_list)
        print(len(command_list), "arcade machines found")

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(command_list))
    command, machine_name, soft_name, driver_name = command_list[rand]
    command_list.pop(rand)

    return command, machine_name, soft_name, driver_name

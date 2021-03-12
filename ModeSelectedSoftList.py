import random
import time

import CommandGeneratorSoftList
import Config
import Display

command_list = []
first_pass = True


def get(machine_list, soft_list_list, soft_list_name_list):
    global command_list
    global first_pass
    if len(command_list) == 0:
        if first_pass is False and Config.auto_quit is True:
            return None, None, None, None
        first_pass = False

        generate_full_command_list(machine_list, soft_list_list, soft_list_name_list)

        if len(command_list) == 0:
            Config.allow_all()

            generate_full_command_list(machine_list, soft_list_list, soft_list_name_list)

    if len(command_list) == 0:
        return None, None, None, None

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(command_list))

    command, machine_name, soft_name, driver_name = command_list[rand]
    command_list.pop(rand)

    return command, machine_name, soft_name, driver_name


def generate_full_command_list(machine_list, soft_list_list, soft_list_name_list):
    global command_list

    for soft_list_name in soft_list_name_list:
        command_list = command_list + CommandGeneratorSoftList.generate_command_list(machine_list, soft_list_list,
                                                                                     soft_list_name)

        Display.print_text("Found " + str(len(command_list)) + " softwares" + Config.get_allowed_string())
        time.sleep(1.5)

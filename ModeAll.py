import random

import CommandGeneratorMachine
import CommandGeneratorSoftList
import Config
import Display

command_list = []
first_pass = True


def get(machine_list, soft_list_list):
    global command_list
    global first_pass
    if len(command_list) == 0:

        if first_pass is False and Config.auto_quit is True:
            return None, None, None, None
        first_pass = False

        command_list = CommandGeneratorMachine.generate_command_list(machine_list)
        Display.print_text("Found " + str(len(command_list)) + " softwares")
        found_qty = len(command_list)
        for soft_list in soft_list_list.findall("softwarelist"):
            command_list = command_list + CommandGeneratorSoftList.generate_command_list(machine_list, soft_list_list,
                                                                                         soft_list.attrib['name'])
            if len(command_list) > found_qty + 1000:
                found_qty = len(command_list)
                Display.print_text("Found " + str(len(command_list)) + " softwares")

        print(len(command_list), "machines or softwares found")

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(command_list))
    command, machine_name, soft_name, driver_name = command_list[rand]
    command_list.pop(rand)

    return command, machine_name, soft_name, driver_name

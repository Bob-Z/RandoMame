import random

import CommandGeneratorMusic

command_list = []


def get(soft_list_list):
    global command_list
    if len(command_list) == 0:
        command_list = CommandGeneratorMusic.generate_music_list(soft_list_list)

    rand = random.randrange(len(command_list))
    command, description = command_list[rand]
    command_list.pop(rand)

    return command, description

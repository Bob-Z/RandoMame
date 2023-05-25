import random

import CommandGeneratorMusic
import Config
import Display
import time

item_list = []
first_pass = True


def get(all_machine_xml, soft_list_list):
    global item_list
    global first_pass
    if len(item_list) == 0:
        if first_pass is False and Config.auto_quit is True:
            return None
        first_pass = False

        item_list = CommandGeneratorMusic.generate_music_list(all_machine_xml, soft_list_list)
        Display.print_text("Found " + str(len(item_list)) + " musics")
        time.sleep(1.5)

    if len(item_list) == 0:
        return None

    if Config.linear is True:
        rand = 0
    else:
        rand = random.randrange(len(item_list))

    selected_item = item_list[rand]
    item_list.pop(rand)
    print(str(len(item_list)), "softwares left")

    return selected_item

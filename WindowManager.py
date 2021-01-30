import threading
import sys

import Command
import Config
import Desktop
import Display
import Window
import Sound
import XmlGetter
import os

from Desktop import DesktopClass
from WindowPosition import WindowPosition


running = True
sound_index = 0


def start():
    window_position = WindowPosition()

    if Config.desktop is not None:
        desktop_info = [Config.desktop[0], Config.desktop[1], Config.desktop[2], Config.desktop[3]]
    else:
        desktop_info = Desktop.get_desktop_size()

    position = window_position.get(Config.windows_quantity, 0, 0, desktop_info[2], desktop_info[3])

    Display.init(desktop_info)

    if Config.mode == "music" or Config.smart_sound_timeout_sec > 0:
        Sound.init()

    machine_list, soft_list = XmlGetter.get()

    if machine_list is not None:
        print("MAME version: ", machine_list.attrib["build"])
        print(len(machine_list), " unique machines")

    if soft_list is not None:
        print(len(soft_list), " softwares lists")

    Command.init(machine_list, soft_list)

    desktop = DesktopClass()

    thread = []
    for index in range(Config.windows_quantity):
        thread.append(threading.Thread(target=Window.manage_window, args=(desktop, index, desktop_info[0], desktop_info[1], position[index],)))
        thread[index].start()

    global sound_index
    while Display.wait_for_keyboard() is False:
        if Config.smart_sound_timeout_sec > 0:
            if Sound.get_silence_duration_sec() > Config.smart_sound_timeout_sec:
                sound_index = sound_index - 1
                if sound_index == -1:
                    sound_index = Config.windows_quantity - 1
                Sound.reset()

    shutdown()

    Sound.kill()

    for t in thread:
        t.join()

    if Config.end_command is not None:
        os.system(Config.end_command)

    sys.exit(0)


def is_running():
    global running
    return running


def shutdown():
    global running
    running = False


def get_sound_index():
    global sound_index
    return sound_index

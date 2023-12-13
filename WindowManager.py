import sys
import time

import Mode
import Config
import Desktop
import Display
import Window
import Sound
import Record
import XmlGetter
import os

from Desktop import DesktopClass
from WindowPosition import WindowPosition


running = True
sound_index = 0
window = []
start_command_launched = False


def start():
    global window

    if Config.windows_quantity == 0:
        machine_list, soft_list = XmlGetter.get()

        if machine_list is not None:
            print("MAME version: ", machine_list.attrib["build"])
            print(len(machine_list), " unique machines")

        if soft_list is not None:
            print(len(soft_list), "software lists")

        Mode.init(machine_list, soft_list)
        Mode.get()

        exit(0)

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
        print(len(soft_list), "software lists")

    Mode.init(machine_list, soft_list)

    desktop = DesktopClass()

    for index in range(Config.windows_quantity):
        window.append(Window.Window(desktop, index, desktop_info[0], desktop_info[1], position[index]))
        time.sleep(1.0)

    global sound_index
    while Display.wait_for_keyboard() is False:
        if Config.smart_sound_timeout_sec > 0:
            if Sound.get_silence_duration_sec() > Config.smart_sound_timeout_sec:
                sound_index = sound_index - 1
                if sound_index == -1:
                    sound_index = Config.windows_quantity - 1

                for w in window:
                    w.set_sound_index(sound_index)

                Sound.reset()

        is_alive = False
        for w in window:
            if w.is_alive() is True:
                is_alive = True
                break

        if is_alive is False:
            break

    if Config.end_duration is not None:
        if Config.record is None:
            time.sleep(float(Config.end_duration))

    if Config.end_command is not None and window[0].get_start_command_launched() is True:
        print("Execute end command:", Config.end_command)
        os.system(Config.end_command)

    print("Shutdown remaining windows")
    shutdown()

    print("Stop sound recording thread")
    Sound.kill()

    print("Wait for remaining windows")
    for w in window:
        w.join()

    if Config.final_command is not None:
        print("Execute final command:", Config.final_command)
        os.system(Config.final_command)

    sys.exit(0)


def shutdown():
    global window
    for w in window:
        w.stop()

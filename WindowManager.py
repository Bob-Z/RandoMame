import sys
import time

import Mode
import Config
import Window
import Sound
import XmlGetter
import os

running = True
sound_index = 0
window = []


def start(main_window):
    global running
    running = True

    if Config.mode == "music" or Config.smart_sound_timeout_sec > 0:
        Sound.init()

    machine_list, soft_list = XmlGetter.get(main_window)

    if machine_list is not None:
        print("MAME version: ", machine_list.attrib["build"])
        print(len(machine_list), " unique machines")

    if soft_list is not None:
        print(len(soft_list), "software lists")

    Mode.init(machine_list, soft_list)

    global window
    for index in range(Config.windows_quantity):
        window.append(Window.Window(main_window.get_single_window(index), index))

    main_window.show_single_windows()

    global sound_index
    while running is True:
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

        time.sleep(0.1)

    if Config.end_command is not None and window[0].get_start_command_launched() is True:
        print("Execute end command:", Config.end_command)
        os.system(Config.end_command)

    print("Shutdown remaining windows")
    shutdown_windows()

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
    global running
    running = False
    for w in window:
        w.kill_mame()


def shutdown_windows():
    global window
    for w in window:
        w.stop()

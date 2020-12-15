import threading
import sys

import Command
import Config
import Desktop
import Display
import Window
import Sound
import time
from Desktop import DesktopClass
from WindowPosition import WindowPosition


running = True
sound_index = 0


def start(machine_list, soft_list, window_qty=1):
    Command.init(machine_list, soft_list)
    window_position = WindowPosition()

    if Config.desktop is not None:
        desktop_info = [Config.desktop[0], Config.desktop[1], Config.desktop[2], Config.desktop[3]]
    else:
        desktop_info = Desktop.get_desktop_size()

    position = window_position.get(window_qty, 0, 0, desktop_info[2], desktop_info[3])

    Display.init()

    desktop = DesktopClass()

    thread = []
    for index in range(window_qty):
        thread.append(threading.Thread(target=Window.manage_window, args=(desktop, index, desktop_info[0], desktop_info[1], position[index],)))
        thread[index].start()

    global sound_index
    while Display.wait_for_keyboard() is False:
        if Sound.get_silence_duration_sec() > Config.smart_sound_timeout_sec:
            sound_index = (sound_index + 1) % window_qty
            print("New sound index:", sound_index)
            Sound.reset()
        time.sleep(0.1)

    shutdown()

    Sound.kill()

    for t in thread:
        t.join()

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

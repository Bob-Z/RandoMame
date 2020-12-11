import threading
import sys

import Command
import Config
import Desktop
import Display
import Window
import Sound
from Desktop import DesktopClass
from WindowPosition import WindowPosition


running = True


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

    Display.wait_for_keyboard()

    Sound.kill()
    shutdown()

    for t in thread:
        t.join()

    sys.exit(0)


def is_running():
    global running
    return running


def shutdown():
    global running
    running = False

import threading

import Command
import Config
import Desktop
import Display
import Window
from Desktop import DesktopClass
from WindowPosition import WindowPosition


def start(machine_list, soft_list, window_qty=1):
    Command.init(machine_list, soft_list)
    window_position = WindowPosition()

    if Config.desktop is not None:
        desktop_info = [Config.desktop[0], Config.desktop[1], Config.desktop[2], Config.desktop[3]]
    else:
        desktop_info = Desktop.get_desktop_size()

    position = window_position.get(window_qty, desktop_info[0], desktop_info[1], desktop_info[2], desktop_info[3])

    Display.init()

    desktop = DesktopClass()

    for index in range(window_qty):
        threading.Thread(target=Window.manage_window, args=(desktop, index, position[index],)).start()

    Display.wait_for_keyboard()

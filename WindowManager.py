import os
import subprocess
import time

import Arcade
import Config
from WindowPosition import WindowPosition


def start(machine_count, root, window_qty=1):
    desktop_w = 1920
    desktop_h = 1080

    size_x = desktop_w / 4
    size_y = desktop_h / 2

    window_position = WindowPosition()
    position = window_position.get(window_qty, 0, 0, 1920, 1080)

    out = []
    machine_name = []

    while True:
        for index in range(window_qty):
            if len(out) > index:
                return_code = out[index].poll()
                if return_code is not None:
                    machine_name[index] = Arcade.get(machine_count, root)
                    out[index] = run_mame(machine_name[index], position[index]['width'], position[index]['height'])
                else:
                    set_position(machine_name[index], position[index]['pos_x'], position[index]['pos_y'])

            else:
                machine_name.append(Arcade.get(machine_count, root))
                out.append(run_mame(machine_name[index], position[index]['width'], position[index]['height']))

        time.sleep(0.2)


def run_mame(machine_name, size_x, size_y):
    size_str = str(int(size_x)) + "x" + str(int(size_y))
    out = subprocess.Popen(
        [Config.mame_binary, "-nohttp", "-window", "-ui_active", "-skip_gameinfo", "-str", str(Config.duration),
         "-resolution",
         size_str, machine_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    return out


def set_position(machine_name, pos_x, pos_y):
    search = "\"MAME.*" + machine_name + "\""
    command = "xdotool search " + search + " windowmove " + str(int(pos_x)) + " " + str(
        int(pos_y))
    os.system(command)

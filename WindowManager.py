import os
import subprocess
import time

import Arcade
import Config


def start(machine_count, root, window_qty=1):
    desktop_w = 1920
    desktop_h = 1080

    size_x = desktop_w / 4
    size_y = desktop_h / 2

    out = []
    while True:
        pos_x = 0
        pos_y = 0
        for index in range(window_qty):
            if len(out) > index:
                return_code = out[index].poll()
                if return_code is not None:
                    machine_name = Arcade.get(machine_count, root)
                    out[index] = run_mame(machine_name, size_x, size_y, pos_x, pos_y)

            else:
                machine_name = Arcade.get(machine_count, root)
                out.append(run_mame(machine_name, size_x, size_y, pos_x, pos_y))

            pos_x += size_x
            if pos_x >= desktop_w:
                pos_x = 0
                pos_y += size_y

        time.sleep(0.1)


def run_mame(machine_name, size_x, size_y, pos_x, pos_y):
    size_str = str(int(size_x)) + "x" + str(int(size_y))
    out = subprocess.Popen(
        [Config.mame_binary, "-nohttp", "-window", "-ui_active", "-skip_gameinfo", "-str", str(Config.duration),
         "-resolution",
         size_str, machine_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    search = "\"MAME.*" + machine_name + "\""
    command = "xdotool search " + search

    try_count = 20
    while try_count > 0:
        exitcode = os.system(command)
        if exitcode == 0:
            command = "xdotool search " + search + " windowmove " + str(int(pos_x)) + " " + str(
                int(pos_y)) + " windowraise"
            os.system(command)
            break
        else:
            time.sleep(0.1)
            try_count = try_count - 1

    return out

import subprocess
import time

import Arcade
import Config
from Desktop import Desktop
from WindowPosition import WindowPosition


def start(machine_count, root, window_qty=1):
    window_position = WindowPosition()
    position = window_position.get(window_qty, 50, 24, 1870, 1056)

    out = []
    machine_name = []
    desktop = Desktop()

    while True:
        for index in range(window_qty):
            if len(out) > index:
                return_code = out[index].poll()
                if return_code is not None:
                    machine_name[index] = Arcade.get(machine_count, root)
                    out[index] = run_mame(machine_name[index])
                else:
                    desktop.send_keyboard(machine_name[index])
                    desktop.set_position(machine_name[index], position[index]['pos_x'], position[index]['pos_y'],
                                         position[index]['width'], position[index]['height'])
            else:
                machine_name.append(Arcade.get(machine_count, root))
                out.append(run_mame(machine_name[index]))

        time.sleep(0.2)


def run_mame(machine_name):
    out = subprocess.Popen(
        [Config.mame_binary, "-artwork_crop", "-nohttp", "-window", "-ui_active", "-skip_gameinfo", "-str",
         str(Config.duration),
         "-resolution",
         "1x1", machine_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    return out

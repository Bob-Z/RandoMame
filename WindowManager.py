import subprocess
import time

import Arcade
import Config
from Desktop import Desktop
from WindowPosition import WindowPosition


def start(machine_count, root, window_qty=1):
    window_position = WindowPosition()

    out = []
    machine_name = []
    desktop = Desktop()

    desktop_info = None
    if Config.desktop is not None:
        split1 = Config.desktop.split('x')
        desktop_info = [int(split1[0]), int(split1[1]), int(split1[2]), int(split1[3])]
    else:
        desktop_info = desktop.get_desktop_size()

    position = window_position.get(window_qty, desktop_info[0], desktop_info[1], desktop_info[2], desktop_info[3])

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
        [Config.mame_binary, "-nomouse", "-artwork_crop", "-nohttp", "-window", "-ui_active", "-skip_gameinfo", "-str",
         str(Config.duration),
         "-resolution",
         "1x1", machine_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    return out

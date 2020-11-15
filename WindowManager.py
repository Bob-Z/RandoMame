import subprocess
import time

import Config
import ModeAll
import ModeArcade
import ModeSelectedSoftList
import ModeSoftList
from Desktop import Desktop
from WindowPosition import WindowPosition


def start(machine_count, machine_list, soft_list_count, soft_list, window_qty=1):
    window_position = WindowPosition()

    out = []
    command = []
    desktop = Desktop()

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
                    out[index] = run_mame(command[index])
                    command[index] = get_command(machine_count, machine_list, soft_list_count, soft_list)

                desktop.send_keyboard(out[index].pid)
                desktop.set_position(out[index].pid, position[index]['pos_x'], position[index]['pos_y'],
                                     position[index]['width'], position[index]['height'])
            else:
                first_command = get_command(machine_count, machine_list, soft_list_count, soft_list)
                out.append(run_mame(first_command))
                command.append(get_command(machine_count, machine_list, soft_list_count, soft_list))

            time.sleep(0.2)


def get_command(machine_count, machine_list, soft_list_count, soft_list):
    if Config.mode == "arcade":
        return ModeArcade.get(machine_count, machine_list)
    elif Config.mode == "softlist":
        return ModeSoftList.get(soft_list_count, machine_list, soft_list)
    elif Config.mode == "all":
        return ModeAll.get(machine_count, machine_list, soft_list_count, soft_list)
    elif Config.mode == "selected softlist":
        return ModeSelectedSoftList.get(Config.selected_softlist, machine_list, soft_list)


def run_mame(command):
    binary_command = Config.mame_binary + " -nomouse -artwork_crop -nohttp -window -ui_active -skip_gameinfo -str " + str(
        Config.duration) + " -resolution 1x1 " + command
    args = [Config.mame_binary, '-nomouse', '-artwork_crop', '-nohttp', '-window',
            '-ui_active', '-skip_gameinfo', '-str', str(
            Config.duration), '-resolution', '1x1']
    for c in command.split(' '):
        args.append(c)

    out = subprocess.Popen(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    return out

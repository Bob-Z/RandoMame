import subprocess
import time

import Config
import ModeAll
import ModeArcade
import ModeSelectedSoftList
import ModeSoftList
from Desktop import Desktop
from WindowPosition import WindowPosition


def start(machine_list, soft_list, window_qty=1):
    window_position = WindowPosition()

    out = []
    title = []
    desktop = Desktop()
    position_done = []
    title_done = []

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
                    command, title[index] = get_command(machine_list, soft_list)
                    out[index] = run_mame(command)
                    title_done[index] = False
                    position_done[index] = False

                desktop.send_keyboard(out[index].pid)
                if position_done[index] is False:
                    position_done[index] = desktop.set_position(out[index].pid, position[index]['pos_x'],
                                                                position[index]['pos_y'],
                                                                position[index]['width'], position[index]['height'])
                if title_done[index] is False:
                    title_done[index] = desktop.set_title(out[index].pid, title[index])
            else:
                first_command, first_title = get_command(machine_list, soft_list)
                title.append(first_title)
                out.append(run_mame(first_command))
                title_done.append(False)
                position_done.append(False)
                break;

        time.sleep(0.2)


def get_command(machine_list, soft_list):
    if Config.mode == "arcade":
        return ModeArcade.get(machine_list)
    elif Config.mode == "softlist":
        return ModeSoftList.get(machine_list, soft_list)
    elif Config.mode == "all":
        return ModeAll.get(machine_list, soft_list)
    elif Config.mode == "selected softlist":
        return ModeSelectedSoftList.get(Config.selected_softlist, machine_list, soft_list)


def run_mame(command):
    if command is None:
        return

    args = [Config.mame_binary]
    for c in command.split(' '):
        args.append(c)
    args += ['-nomouse', '-artwork_crop', '-nohttp', '-window',
             '-ui_active', '-skip_gameinfo', '-str', str(Config.duration), '-resolution', '1x1']

    full_command = ""
    for a in args:
        full_command += a + " "
    print("Running full command: " + full_command)

    out = subprocess.Popen(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    return out

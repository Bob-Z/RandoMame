import subprocess
import time

import Config
import ModeAll
import ModeArcade
import ModeSelectedSoftList
import ModeSoftList
import ModeMusic
from Desktop import Desktop
from WindowPosition import WindowPosition


def start(machine_list, soft_list, window_qty=1):
    window_position = WindowPosition()

    out = []
    title = []
    desktop = Desktop()
    command = []

    if Config.desktop is not None:
        split1 = Config.desktop.split('x')
        desktop_info = [int(split1[0]), int(split1[1]), int(split1[2]), int(split1[3])]
    else:
        desktop_info = desktop.get_desktop_size()

    position = window_position.get(window_qty, desktop_info[0], desktop_info[1], desktop_info[2], desktop_info[3])

    count = 20

    while True:
        for index in range(window_qty):
            if len(out) > index:
                while out[index].poll() is not None:
                    out[index] = run_mame(command[index])

                    while desktop.set_title(out[index].pid, title[index]) is False:
                        if out[index].poll() is not None:
                            break

                    while desktop.set_position(out[index].pid, position[index]['pos_x'],
                                               position[index]['pos_y'],
                                               position[index]['width'], position[index]['height']) is False:
                        if out[index].poll() is not None:
                            break

                    command[index], title[index] = get_command(machine_list, soft_list)

                if count == 0:
                    desktop.send_keyboard(out[index].pid)
                    count = 20
                else:
                    count = count - 1

            else:
                first_command, first_title = get_command(machine_list, soft_list)
                out.append(run_mame(first_command))
                while desktop.set_title(out[index].pid, first_title) is False:
                    if out[index].poll() is not None:
                        break

                while desktop.set_position(out[index].pid, position[index]['pos_x'],
                                           position[index]['pos_y'],
                                           position[index]['width'], position[index]['height']) is False:
                    if out[index].poll() is not None:
                        break
                    pass
                next_command, next_title = get_command(machine_list, soft_list)
                command.append(next_command)
                title.append(next_title)

        time.sleep(0.1)


def get_command(machine_list, soft_list):
    if Config.mode == "arcade":
        return ModeArcade.get(machine_list)
    elif Config.mode == "softlist":
        return ModeSoftList.get(machine_list, soft_list)
    elif Config.mode == "all":
        return ModeAll.get(machine_list, soft_list)
    elif Config.mode == "selected softlist":
        return ModeSelectedSoftList.get(machine_list, soft_list, Config.selected_softlist)
    elif Config.mode == "music":
        return ModeMusic.get(soft_list)


def run_mame(command):
    if command is None:
        return

    args = [Config.mame_binary]
    for c in command.split(' '):
        args.append(c)
    args += ['-nomouse', '-nohttp', '-window',
             '-ui_active', '-skip_gameinfo', '-str', str(Config.duration), '-resolution', '1x1']

    if Config.mode != 'music':
        args += '-artwork_crop'

    full_command = ""
    for a in args:
        full_command += a + " "
    print("Running full command: " + full_command)

    out = subprocess.Popen(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    return out

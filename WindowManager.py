import datetime
import os
import subprocess
import time

import Config
import ModeAll
import ModeArcade
import ModeMusic
import ModeSelectedSoftList
import ModeSoftList
import Sound
from Desktop import Desktop
from WindowPosition import WindowPosition


def start(machine_list, soft_list, window_qty=1):
    window_position = WindowPosition()

    out = []
    title = []
    desktop = Desktop()
    command = []
    date = []

    if Config.desktop is not None:
        desktop_info = [Config.desktop[0], Config.desktop[1], Config.desktop[2], Config.desktop[3]]
    else:
        desktop_info = desktop.get_desktop_size()

    position = window_position.get(window_qty, desktop_info[0], desktop_info[1], desktop_info[2], desktop_info[3])

    count = 20

    while True:
        for index in range(window_qty):
            if len(out) > index:
                if Config.mode == 'music':
                    sdet = Sound.is_silence_detected()
                    if sdet is True:
                        out[index].kill()
                        Sound.reset()

                if date[index] < datetime.datetime.now():
                    out[index].kill()
                    Sound.reset()

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

                    date[index] = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout)

                if count == 0:
                    desktop.send_keyboard(out[index].pid)
                    count = 10
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

                next_command, next_title = get_command(machine_list, soft_list)
                command.append(next_command)
                title.append(next_title)
                date.append(datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout))

                if Config.mode == 'music':
                    Sound.reset()

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
             '-ui_active', '-skip_gameinfo', '-resolution', '1x1']
    # '-str', str(Config.duration),

    if Config.mode != 'music':
        args.append('-artwork_crop')

    full_command = ""
    for a in args:
        full_command += a + " "
    print("Running full command: " + full_command)

    # Linux PulseAudio specific
    my_env = os.environ.copy()
    my_env["XDG_RUNTIME_DIR"] = "/run/user/" + str(os.getuid())

    out = subprocess.Popen(args,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           env=my_env)

    Sound.reset()

    return out

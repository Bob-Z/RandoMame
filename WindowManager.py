import datetime
import os
import subprocess
import threading
import time

import pygame

import Config
import Desktop
import ModeAll
import ModeArcade
import ModeMusic
import ModeSelectedSoftList
import ModeSoftList
import Sound
from Desktop import DesktopClass
from WindowPosition import WindowPosition

my_machine_list = []
my_soft_list = []
desktop = DesktopClass()


def start(machine_list, soft_list, window_qty=1):
    global my_machine_list
    my_machine_list = machine_list
    global my_soft_list
    my_soft_list = soft_list

    window_position = WindowPosition()

    if Config.desktop is not None:
        desktop_info = [Config.desktop[0], Config.desktop[1], Config.desktop[2], Config.desktop[3]]
    else:
        desktop_info = Desktop.get_desktop_size()

    position = window_position.get(window_qty, desktop_info[0], desktop_info[1], desktop_info[2], desktop_info[3])

    for index in range(window_qty):
        threading.Thread(target=manage_window, args=(index, position[index],)).start()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            exit(0)


def manage_window(index, position):
    global desktop

    first_command, first_title = get_command()
    out = run_mame(first_command)
    while desktop.set_title(out.pid, first_title) is False:
        if out.poll() is not None:
            break

    while desktop.set_position(out.pid, position['pos_x'],
                               position['pos_y'],
                               position['width'], position['height']) is False:
        if out.poll() is not None:
            break

    command, title = get_command()
    delay_start = Config.timeout / Config.windows_quantity
    date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout) + datetime.timedelta(
        seconds=(index * delay_start))

    if Config.mode == 'music':
        Sound.reset()

    count = 0
    while True:
        if Config.mode == 'music':
            silence_detected = Sound.is_silence_detected()
            if silence_detected is True:
                out.kill()
                Sound.reset()

        if date < datetime.datetime.now():
            out.kill()
            Sound.reset()

        while out.poll() is not None:
            count = 0
            out = run_mame(command)

            while desktop.set_title(out.pid, title) is False:
                if out.poll() is not None:
                    break

            while desktop.set_position(out.pid, position['pos_x'],
                                       position['pos_y'],
                                       position['width'], position['height']) is False:
                if out.poll() is not None:
                    break

            command, title = get_command()
            date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout)

            count = 0

        if count == 0:
            desktop.send_keyboard(out.pid)
            count = 20
        else:
            count = count - 1

        time.sleep(0.1)


gen_lock = threading.Lock()


def get_command():
    global my_machine_list
    global my_soft_list
    global gen_lock
    with gen_lock:
        if Config.mode == "arcade":
            return ModeArcade.get(my_machine_list)
        elif Config.mode == "softlist":
            return ModeSoftList.get(my_machine_list, my_soft_list)
        elif Config.mode == "all":
            return ModeAll.get(my_machine_list, my_soft_list)
        elif Config.mode == "selected softlist":
            return ModeSelectedSoftList.get(my_machine_list, my_soft_list, Config.selected_softlist)
        elif Config.mode == "music":
            return ModeMusic.get(my_soft_list)


def run_mame(command):
    if command is None:
        return

    args = [Config.mame_binary]
    for c in command.split(' '):
        args.append(c)
    args += ['-nomouse', '-nohttp', '-window',
             '-ui_active', '-skip_gameinfo', '-resolution', '1x1']

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

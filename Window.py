import datetime
import time

import Command
import Config
import Display
import Mame
import Sound
import WindowManager


def manage_window(desktop, index, desktop_offset_x, desktop_offset_y, position):
    first_command, first_machine_name, first_soft_name = Command.get()

    Display.print_window(first_machine_name, first_soft_name, 32, position)
    time.sleep(2)

    out = Mame.run(first_command)

    if first_soft_name is not None:
        first_title = first_soft_name + " // " + first_machine_name
    else:
        first_title = first_machine_name

    while desktop.set_title(out.pid, first_title) is False:
        if out.poll() is not None:
            break

    while desktop.set_position(out.pid, desktop_offset_x + position['pos_x'],
                               desktop_offset_y + position['pos_y'],
                               position['width'], position['height']) is False:
        if out.poll() is not None:
            break

    command, machine_name, soft_name = Command.get()
    Display.print_window(machine_name, soft_name, 32, position)

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
            time.sleep(2)
            out = Mame.run(command)

            if soft_name is not None:
                title = soft_name + " // " + machine_name
            else:
                title = machine_name

            while desktop.set_title(out.pid, title) is False:
                if out.poll() is not None:
                    break

            while desktop.set_position(out.pid, desktop_offset_x + position['pos_x'],
                                       desktop_offset_y + position['pos_y'],
                                       position['width'], position['height']) is False:
                if out.poll() is not None:
                    break

            command, machine_name, soft_name = Command.get()
            date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout)

            Display.print_window(machine_name, soft_name, 32, position)

            count = 0

        if count <= 0:
            desktop.send_keyboard(out.pid)
            count = 20
        else:
            count = count - 1

        time.sleep(0.1)

        if WindowManager.is_running() is False:
            out.kill()
            break

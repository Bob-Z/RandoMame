import datetime
import time

import Command
import Config
import Display
import Mame
import Sound
import os
import WindowManager

auto_keyboard_timeout = None
auto_keyboard_date = None


def manage_window(desktop, index, desktop_offset_x, desktop_offset_y, position):
    first_command, first_machine_name, first_soft_name, first_driver = Command.get()

    if first_command is None:
        print("No software for window", index)
        return

    Display.print_window(first_machine_name, first_soft_name, position, first_driver)
    time.sleep(1.5)

    out = Mame.run(first_command)

    if first_soft_name is not None:
        title = first_soft_name + " // " + first_machine_name
    else:
        title = first_machine_name

    while desktop.set_title(out.pid, title) is False:
        if out.poll() is not None:
            break

    while desktop.set_position(out.pid, desktop_offset_x + position['pos_x'],
                               desktop_offset_y + position['pos_y'],
                               position['width'], position['height']) is False:
        if out.poll() is not None:
            break

    if Config.smart_sound_timeout_sec > 0:
        if index == 0:
            Sound.set_mute(out.pid, False)
            is_muted = False
        else:
            Sound.set_mute(out.pid, True)
            is_muted = True

    command, machine_name, soft_name, driver_name = Command.get()
    if command is None:
        print("No more software for window", index)
        Display.print_window("No more software", None, position)
        return

    Display.print_window(machine_name, soft_name, position, driver_name)

    delay_start = Config.timeout / Config.windows_quantity
    date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout) + datetime.timedelta(
        seconds=(index * delay_start))

    global auto_keyboard_timeout
    auto_keyboard_timeout = 1.0
    global auto_keyboard_date
    auto_keyboard_date = datetime.datetime.now()

    if Config.mode == 'music':
        Sound.reset()

    while True:
        if Config.mode == 'music':
            if Sound.get_silence_duration_sec() > 5.0:
                out.kill()
                Sound.reset()

        if date < datetime.datetime.now():
            out.kill()
            Sound.reset()

        while out.poll() is not None:
            time.sleep(1.5)
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

            if Config.smart_sound_timeout_sec > 0:
                Sound.set_mute(out.pid, True)
                desktop.set_title(out.pid, title)
                is_muted = True

            date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout)
            auto_keyboard_timeout = 1.0
            auto_keyboard_date = datetime.datetime.now()

            command, machine_name, soft_name, driver_name = Command.get()
            if command is None:
                print("No more software for window", index)
                Display.print_window("No more software", None, position)

                while WindowManager.is_running() is True and send_keyboard(desktop, out.pid) is True:
                    time.sleep(0.1)

                return

            Display.print_window(machine_name, soft_name, position, driver_name)

        send_keyboard(desktop, out.pid)

        if Config.smart_sound_timeout_sec > 0:
            if WindowManager.get_sound_index() == index:
                if is_muted is True:
                    Sound.set_mute(out.pid, False)
                    desktop.set_title(out.pid, "* " + title)
                    is_muted = False
            else:
                if is_muted is False:
                    Sound.set_mute(out.pid, True)
                    desktop.set_title(out.pid, title)
                    is_muted = True

        time.sleep(0.1)

        if WindowManager.is_running() is False:
            out.kill()
            break


def send_keyboard(desktop, pid):
    global auto_keyboard_timeout
    global auto_keyboard_date

    if auto_keyboard_timeout > 0:
        if datetime.datetime.now() > auto_keyboard_date + datetime.timedelta(seconds=auto_keyboard_timeout):
            desktop.send_keyboard(pid)
            auto_keyboard_timeout = auto_keyboard_timeout + 1
            if auto_keyboard_timeout > 15:
                auto_keyboard_timeout = 0
        return True
    else:
        return False

import datetime
import os
import threading
import time

import Command
import Config
import Display
import Mame
import Sound


class Window:
    def __init__(self, desktop, index, desktop_offset_x, desktop_offset_y, position):
        self.auto_keyboard_timeout = 1.0
        self.auto_keyboard_date = None
        self.desktop = desktop
        self.index = index
        self.desktop_offset_x = desktop_offset_x
        self.desktop_offset_y = desktop_offset_y
        self.position = position
        self.sound_index = 0

        self.thread = threading.Thread(target=Window.manage_window, args=(self,))
        self.thread.start()
        self.is_running = True
        self.is_muted = True
        self.out = None

    def stop(self):
        self.is_running = False

    def is_alive(self):
        return self.thread.is_alive()

    def join(self):
        return self.thread.join()

    def set_sound_index(self, sound_index):
        self.sound_index = sound_index

    def manage_window(self):
        first_command, first_machine_name, first_soft_name, first_driver_name_list = Command.get()

        if first_command is None:
            print("No software for window", self.index)
            return

        Display.print_window(first_machine_name, first_soft_name, self.position, first_driver_name_list)
        if Config.start_command is not None and self.index == 0:
            os.system(Config.start_command)

        time.sleep(1.5)

        self.out = Mame.run(first_command)

        if first_soft_name is not None:
            title = first_soft_name + " // " + first_machine_name
        else:
            title = first_machine_name

        while self.desktop.set_title(self.out.pid, title) is False:
            if self.out.poll() is not None:
                break

        while self.desktop.set_position(self.out.pid, self.desktop_offset_x + self.position['pos_x'],
                                        self.desktop_offset_y + self.position['pos_y'],
                                        self.position['width'], self.position['height']) is False:
            if self.out.poll() is not None:
                break

        if Config.smart_sound_timeout_sec > 0:
            if self.index == 0:
                Sound.set_mute(self.out.pid, False)
                self.is_muted = False
            else:
                Sound.set_mute(self.out.pid, True)
                self.is_muted = True

        command, machine_name, soft_name, driver_name_list = Command.get()
        if command is None:
            print("No more software for window", self.index)
            Display.print_window("No more software", None, self.position, driver_name_list)
            return

        Display.print_window(machine_name, soft_name, self.position, driver_name_list)

        delay_start = Config.timeout / Config.windows_quantity
        date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout) + datetime.timedelta(
            seconds=(self.index * delay_start))

        self.auto_keyboard_date = 1.0
        self.auto_keyboard_date = datetime.datetime.now()

        is_sound_started = False

        while True:
            if Config.mode == 'music':
                if Sound.get_silence_duration_sec() == 0:
                    is_sound_started = True

                if is_sound_started is True and Sound.get_silence_duration_sec() > 5.0:
                    self.out.kill()
                    is_sound_started = False

            if date < datetime.datetime.now():
                self.out.kill()
                Sound.reset()

            while self.out.poll() is not None:
                time.sleep(1.5)
                self.out = Mame.run(command)

                if soft_name is not None:
                    title = soft_name + " // " + machine_name
                else:
                    title = machine_name

                while self.desktop.set_title(self.out.pid, title) is False:
                    if self.out.poll() is not None:
                        break

                while self.desktop.set_position(self.out.pid, self.desktop_offset_x + self.position['pos_x'],
                                                self.desktop_offset_y + self.position['pos_y'],
                                                self.position['width'], self.position['height']) is False:
                    if self.out.poll() is not None:
                        break

                if Config.smart_sound_timeout_sec > 0:
                    Sound.set_mute(self.out.pid, True)
                    self.desktop.set_title(self.out.pid, title)
                    self.is_muted = True

                date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout)
                self.auto_keyboard_date = 1.0
                self.auto_keyboard_date = datetime.datetime.now()

                command, machine_name, soft_name, driver_name_list = Command.get()
                if command is None:
                    print("No more software for window", self.index)
                    Display.print_window("No more software", None, self.position, driver_name_list)

                    while self.is_running is True:
                        self.send_keyboard()

                        if Config.mode == 'music':
                            if Sound.get_silence_duration_sec() == 0:
                                is_sound_started = True

                            if is_sound_started is True and Sound.get_silence_duration_sec() > 5.0:
                                self.out.kill()
                                is_sound_started = False

                        if date < datetime.datetime.now():
                            self.out.kill()
                            Sound.reset()

                        time.sleep(0.1)
                        if self.out.poll() is not None:
                            return

                    self.out.kill()
                    return

                Display.print_window(machine_name, soft_name, self.position, driver_name_list)

                is_sound_started = False

            self.send_keyboard()

            if Config.smart_sound_timeout_sec > 0:
                if self.sound_index == self.index:
                    if self.is_muted is True:
                        Sound.set_mute(self.out.pid, False)
                        self.desktop.set_title(self.out.pid, "* " + title)
                        self.is_muted = False
                else:
                    if self.is_muted is False:
                        Sound.set_mute(self.out.pid, True)
                        self.desktop.set_title(self.out.pid, title)
                        self.is_muted = True

            time.sleep(0.1)

            if self.is_running is False:
                self.out.kill()
                break

    def send_keyboard(self):

        if self.auto_keyboard_timeout > 0:
            if datetime.datetime.now() > self.auto_keyboard_date + datetime.timedelta(
                    seconds=self.auto_keyboard_timeout):
                self.desktop.send_keyboard(self.out.pid)
                auto_keyboard_timeout = self.auto_keyboard_timeout + 1
                if auto_keyboard_timeout > 15:
                    self.auto_keyboard_timeout = 0
            return True
        else:
            return False

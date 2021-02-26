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
        self.first_launch = True

        self.desktop = desktop
        self.index = index
        self.desktop_offset_x = desktop_offset_x
        self.desktop_offset_y = desktop_offset_y
        self.position = position
        self.sound_index = 0

        self.is_running = True
        self.is_muted = False
        self.out = None

        self.command = None
        self.machine_name = None
        self.soft_name = None
        self.driver_name_list = None
        self.title = None

        self.auto_keyboard_timeout = 1.0
        self.auto_keyboard_date = None
        self.end_date = None

        self.is_sound_started = False

        self.thread_running = True
        self.thread = threading.Thread(target=Window.manage_window, args=(self,))
        self.thread.start()

        self.start_command_launched = False

    def manage_window(self):
        if self.get_command() is False:
            return

        self.launch_mame()

        while self.thread_running is True:
            self.launch_mame()

            self.manage_silence()

            self.manage_date()

            self.send_keyboard()

            self.manage_smart_sound()

            self.manage_stop()

            time.sleep(0.1)

    def launch_mame(self):
        while self.out is None or self.out.poll() is not None:

            if self.command is None:
                return

            wait_loop = 15
            while wait_loop > 0:
                time.sleep(0.1)
                wait_loop = wait_loop - 1
                if self.is_running is False:
                    return

            self.out = Mame.run(self.command)

            self.set_title()

            self.set_position()

            self.init_smart_sound()

            self.init_silence()

            self.init_date()

            self.first_launch = False

            self.get_command()

    def set_title(self):
        if self.soft_name is not None:
            self.title = self.soft_name + " // " + self.machine_name
        else:
            self.title = self.machine_name

        while self.desktop.set_title(self.out.pid, self.title) is False:
            if self.out.poll() is not None:
                break

    def set_position(self):
        while self.desktop.set_position(self.out.pid, self.desktop_offset_x + self.position['pos_x'],
                                        self.desktop_offset_y + self.position['pos_y'],
                                        self.position['width'], self.position['height']) is False:
            if self.out.poll() is not None:
                break

    def init_date(self):
        if self.first_launch is True:
            delay_start = Config.timeout / Config.windows_quantity
        else:
            delay_start = 0

        self.end_date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout) + datetime.timedelta(
            seconds=(self.index * delay_start))
        self.auto_keyboard_date = 1.0
        self.auto_keyboard_date = datetime.datetime.now()

    def manage_date(self):
        if self.end_date < datetime.datetime.now():
            self.out.kill()
            Sound.reset()

    def get_command(self):
        self.command, self.machine_name, self.soft_name, self.driver_name_list = Command.get()
        if self.command is None:
            print("No more software for window", self.index)
            Display.print_window(" ", None, self.position, self.driver_name_list)
            return False
        else:
            Display.print_window(self.machine_name, self.soft_name, self.position, self.driver_name_list)

            if self.first_launch is True:
                if Config.start_command is not None and self.index == 0:
                    print("Execute start command:", Config.start_command)
                    os.system(Config.start_command)
                    self.start_command_launched = True

            return True

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

    def init_silence(self):
        self.is_sound_started = False

    def manage_silence(self):
        if Config.mode == 'music':
            if Sound.get_silence_duration_sec() == 0:
                self.is_sound_started = True

            if self.is_sound_started is True and Sound.get_silence_duration_sec() > 5.0:
                self.out.kill()
                self.is_sound_started = False

    def init_smart_sound(self):
        if Config.mode == 'music':
            Sound.set_mute(self.out.pid, False)
            self.is_muted = False
        else:
            if Config.smart_sound_timeout_sec > 0:
                Sound.set_mute(self.out.pid, True)
                self.is_muted = True

    def manage_smart_sound(self):
        if Config.smart_sound_timeout_sec > 0:
            if self.sound_index == self.index:
                if self.is_muted is True:
                    Sound.set_mute(self.out.pid, False)
                    self.desktop.set_title(self.out.pid, "* " + self.title)
                    self.is_muted = False
            else:
                if self.is_muted is False:
                    Sound.set_mute(self.out.pid, True)
                    self.desktop.set_title(self.out.pid, self.title)
                    self.is_muted = True

    def manage_stop(self):
        if self.is_running is False:
            self.out.kill()
            self.thread_running = False

        if self.command is None:
            if self.out.poll() is not None:
                self.thread_running = False

    def stop(self):
        self.is_running = False

    def is_alive(self):
        return self.thread.is_alive()

    def join(self):
        return self.thread.join()

    def set_sound_index(self, sound_index):
        self.sound_index = sound_index

    def get_start_command_launched(self):
        return self.start_command_launched

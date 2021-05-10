import datetime
import os
import threading
import time

import Config
import Display
import Mame
import Mode
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

        self.item = None
        self.title = None

        self.auto_keyboard_date = None
        self.end_date = None

        self.is_sound_started = False

        self.send_keyboard_skip = True

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

            if self.item is None:
                return

            wait_loop = 15
            while wait_loop > 0:
                time.sleep(0.1)
                wait_loop = wait_loop - 1
                if self.is_running is False:
                    return

            self.out = Mame.run(self.item)

            self.set_title()

            self.set_position()

            self.init_smart_sound()

            self.init_silence()

            self.init_date()

            self.first_launch = False

            self.get_command()

            self.send_keyboard_skip = True

    def set_title(self):
        self.title = self.item.get_title()

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

        self.auto_keyboard_date = datetime.datetime.now()

    def manage_date(self):
        if self.end_date < datetime.datetime.now():
            self.out.kill()

            Sound.reset()

    def get_command(self):
        self.item = Mode.get()
        if self.item is None:
            print("No more software for window", self.index)
            Display.print_machine_and_soft(None, self.position)
            return False
        else:
            Display.print_machine_and_soft(self.item, self.position)

            if self.first_launch is True:
                if Config.start_command is not None and self.index == 0:
                    print("Execute start command:", Config.start_command)
                    os.system(Config.start_command)
                    self.start_command_launched = True

            if Config.record is not None:
                Display.record_window()

            return True

    def send_keyboard(self):
        if self.send_keyboard_skip is True:
            self.desktop.send_keyboard(self.out.pid, "Hyper_L")
            if datetime.datetime.now() > self.auto_keyboard_date + datetime.timedelta(
                    seconds=15):
                self.send_keyboard_skip = False

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

        if self.item is None:
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

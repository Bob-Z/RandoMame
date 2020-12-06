import time
import Command
import Config
import datetime
import Sound
import Mame
import WindowManager


def manage_window(desktop, index, position):
    first_command, first_title = Command.get()
    out = Mame.run(first_command)
    while desktop.set_title(out.pid, first_title) is False:
        if out.poll() is not None:
            break

    while desktop.set_position(out.pid, position['pos_x'],
                               position['pos_y'],
                               position['width'], position['height']) is False:
        if out.poll() is not None:
            break

    command, title = Command.get()
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
            out = Mame.run(command)

            while desktop.set_title(out.pid, title) is False:
                if out.poll() is not None:
                    break

            while desktop.set_position(out.pid, position['pos_x'],
                                       position['pos_y'],
                                       position['width'], position['height']) is False:
                if out.poll() is not None:
                    break

            command, title = Command.get()
            date = datetime.datetime.now() + datetime.timedelta(seconds=Config.timeout)

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

import DesktopXfce
from DesktopXfce import Xfce


def get_desktop_size():
    return DesktopXfce.get_desktop_size()


class DesktopClass:
    desktop = None

    def __init__(self):
        self.desktop = Xfce()

    def set_position(self, pid, pos_x, pos_y, width, height):
        return self.desktop.set_position(pid, pos_x, pos_y, width, height)

    def send_keyboard(self, pid):
        return self.desktop.send_keyboard(pid)

    def set_title(self, pid, title):
        return self.desktop.set_title(pid, title)

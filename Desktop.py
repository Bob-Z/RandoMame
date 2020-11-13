from DesktopXfce import DesktopXfce


class Desktop:
    desktop = None

    def __init__(self):
        self.desktop = DesktopXfce()

    def get_desktop_size(self):
        return self.desktop.get_desktop_size()

    def set_position(self, pid, pos_x, pos_y, width, height):
        self.desktop.set_position(pid, pos_x, pos_y, width, height)

    def send_keyboard(self, pid):
        self.desktop.send_keyboard(pid)

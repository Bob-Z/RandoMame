from DesktopXfce import DesktopXfce


class Desktop:
    desktop = None

    def __init__(self):
        self.desktop = DesktopXfce()

    def set_position(self, machine_name, pos_x, pos_y, width, height):
        self.desktop.set_position(machine_name, pos_x, pos_y, width, height)

    def send_keyboard(self, machine_name):
        self.desktop.send_keyboard(machine_name)

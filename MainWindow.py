import sys
from PyQt6.QtWidgets import QMainWindow, QGridLayout
from PyQt6.QtWidgets import QWidget

import Config
import WindowManager
from MarqueeWindow import MarqueeWindow
from SingleWindow import SingleWindow


def get_geometry(target_width, target_height):
    quantity = Config.windows_quantity

    target_ratio = target_width / target_height
    best_x = 0
    best_y = 0
    best_diff = 99999.0
    for x in range(1, quantity + 1):
        if (quantity % x) != 0:
            continue
        y = quantity / x

        ratio = (x * 4) / (y * 3)  # TODO hard coded ratio 4:3
        diff = abs(ratio - target_ratio)
        if diff < best_diff:
            best_diff = diff
            best_x = x
            best_y = y

    return [int(best_x), int(best_y)]


class MainWindow(QMainWindow):
    def __init__(self, application):
        super().__init__()

        # self.setStyleSheet("background-color: black;")
        self.setWindowTitle("RandoMame")
        self.setGeometry(400, 400, 800, 600)

        self.SingleWindowParent = QWidget(self)
        self.layout = QGridLayout(self.SingleWindowParent)

        self.grid_layout = get_geometry(self.geometry().x(), self.geometry().y())

        self.single_window = []
        for x in range(0, self.grid_layout[0] * self.grid_layout[1]):
            self.single_window.append(SingleWindow(self.SingleWindowParent, application))

        self.BackgroundWindow = MarqueeWindow(self)

        self.SingleWindowParent.hide()
        self.BackgroundWindow.show()

    def resizeEvent(self, event):
        self.grid_layout = get_geometry(event.size().width(), event.size().height())

        index = 0

        for x in range(0, self.grid_layout[0]):
            for y in range(0, self.grid_layout[1]):
                self.layout.addWidget(self.single_window[index], y, x)
                index = index + 1

        self.SingleWindowParent.resize(event.size())

        self.BackgroundWindow.resize(event.size())

    def setText(self, text):
        self.BackgroundWindow.setText(text)

    def get_single_window(self, index):
        return self.single_window[index]

    def show_single_windows(self):
        self.BackgroundWindow.hide()
        self.SingleWindowParent.show()

    def closeEvent(self, e):
        print("MainWindow close")
        WindowManager.shutdown()
        for w in self.single_window:
            w.closeEvent(e)

    def keyPressEvent(self, event):
        print("MainWindow", event.text())
        super().keyPressEvent(event)

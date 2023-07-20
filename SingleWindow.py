import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QKeyEvent
from MarqueeWindow import MarqueeWindow


class SingleWindow(QWidget):
    def __init__(self, parent, application):
        super().__init__(parent)

        self.application = application

        self.mame = QWidget(self)
        #self.mame.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.window_id = (int(self.mame.winId()))

        self.marquee = MarqueeWindow(self)
        #self.marquee.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # self.layout = QLayout(self)
        # self.layout.addWidget(self.text_label)
        # QLayout.setAlignment(self.layout, Qt.AlignmentFlag.AlignCenter)

    def resizeEvent(self, event):
        self.marquee.resizeEvent(event)
        self.mame.resize(event.size())

        # self.grab().save("image.png")

    #    def paintEvent(self, event):
    #        self.label.setPixmap(self.background.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def setText(self, text):
        self.marquee.setText(text)

    def clear(self):
        self.marquee.clear()

    def set_pixmap(self, filename):
        self.marquee.set_pixmap(filename)

    def get_window_id(self):
        return self.window_id

    def send_keyboard(self):
        evt1 = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Hyper_L, Qt.KeyboardModifier.NoModifier)
        evt2 = QKeyEvent(QEvent.Type.KeyRelease, Qt.Key.Key_Hyper_L, Qt.KeyboardModifier.NoModifier)

        # self.MameWindow.setFocus()
        self.application.postEvent(self.mame, evt1)
        self.application.postEvent(self.mame, evt2)

    def keyPressEvent(self, event):
        print("SingleWindow", event.text())
        self.marquee.keyPressEvent(event)
        self.mame.keyPressEvent(event)
        super().keyPressEvent(event)

    def show_mame(self):
        self.mame.hide()
        self.mame.show()
        self.mame.setFocus()
        #super().layout().activate()

    def closeEvent(self, e):
        print("SingleWindow close")


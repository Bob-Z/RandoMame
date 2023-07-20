import sys
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QKeyEvent


class MarqueeWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.background_pixmap = QPixmap("/media/4To/emu/mame/mame.png")

        self.pixmap_label = QLabel(self)
        self.pixmap_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmap_label.setStyleSheet("background-color: black;")

        self.text_label = QLabel(self)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setStyleSheet("color: white;")
        #self.text_label.setText("toto")
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.font = self.text_label.font()
        self.text_label.setWordWrap(True)

    def resizeEvent(self, event):
        self.pixmap_label.resize(event.size())
        self.pixmap_label.setPixmap(self.background_pixmap.scaled(event.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.pixmap_label.show()

        self.text_label.resize(event.size())
        self.font.setPointSize(50)
        self.text_label.setFont(self.font)

        # self.grab().save("image.png")

    #    def paintEvent(self, event):
    #        self.label.setPixmap(self.background.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def setText(self, text):
        self.text_label.setText(text)

    def clear(self):
        self.pixmap_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))
        self.text_label("")

    def set_pixmap(self, filename):
        pixmap = QPixmap(filename)
        self.pixmap_label.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def keyPressEvent(self, event):
        print("MarqueeWindow", event.text())
        super().keyPressEvent(event)

    def closeEvent(self, e):
        print("MarqueeWindow close")

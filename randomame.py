#!/usr/bin/python3

import sys
import Check
import Config
import DisplaySoftList
import WindowManager
from MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import threading

Config.parse_command_line()

if Config.available_softlist is True:
    DisplaySoftList.display_soft_list()
    exit(0)

if Config.check is not None:
    Check.start()
else:
    application = QApplication.instance()
    if not application:
        application = QApplication(sys.argv)

    main = MainWindow(application)
    main.show()

    t1 = threading.Thread(target=WindowManager.start, args=(main,))
    t1.start()

    print("Start Qt")
    application.exec()

    t1.join()

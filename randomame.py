#!/usr/bin/python3

import Config
import DisplaySoftList
import WindowManager


Config.parse_command_line()

if Config.available_softlist is True:
    DisplaySoftList.display_soft_list()
    exit(0)

WindowManager.start()

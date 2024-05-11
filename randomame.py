#!/usr/bin/python3

import Check
import Config
import DisplaySoftList
import WindowManager

Config.parse_command_line()

if Config.available_softlist is True:
    DisplaySoftList.display_soft_list()
    exit(0)

if Config.check is not None:
    Check.start()
elif Config.print_file is True:
    Check.print_file_tree()
else:
    WindowManager.start()

#!/usr/bin/python3

import Config
import DisplaySoftList
import WindowManager
import XmlGetter

Config.parse_command_line()

if Config.available_softlist is True:
    DisplaySoftList.display_soft_list()
    exit(0)

machine_list, soft_list = XmlGetter.get()

print("MAME version: ", machine_list.attrib["build"])

print(len(machine_list), " unique machines")

if Config.need_softlist:
    print(len(soft_list), " softwares lists")

WindowManager.start(machine_list, soft_list, Config.windows_quantity)

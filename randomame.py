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

machine_count = 0
arcade_count = 0
non_arcade_count = 0
no_input_machine = 0

for machine in machine_list.findall('machine'):
    machine_input = machine.find('input')
    if machine_input is not None:
        if "coins" in machine_input.attrib:
            arcade_count += 1
        else:
            non_arcade_count += 1
    else:
        no_input_machine += 1

print(len(machine_list), " unique machines")
print(arcade_count, " arcade machines")
print(non_arcade_count, " non arcade machines")
print(no_input_machine, " machine without input")

if Config.need_softlist:
    print(len(soft_list), " softwares lists")

WindowManager.start(machine_list, soft_list, Config.windows_quantity)

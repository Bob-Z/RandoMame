#!/usr/bin/python3

import Config
import WindowManager
from XmlGetter import XmlGetter

Config.parse_command_line()

xml_getter = XmlGetter()
machine_list, soft_list = xml_getter.get()

print("MAME version: ", machine_list.attrib["build"])

machine_count = 0
arcade_count = 0
non_arcade_count = 0
no_input_machine = 0

for machine in machine_list.findall('machine'):
    machine_count += 1

machine_input = machine.find('input')
if machine_input is not None:
    if "coins" in machine_input.attrib:
        arcade_count += 1
    else:
        non_arcade_count += 1
else:
    no_input_machine += 1

print(machine_count, " unique machines")
print(arcade_count, " arcade machines")
print(non_arcade_count, " non arcade machines")
print(no_input_machine, " machine without input")

soft_list_count = 0
if Config.mode == "softlist":
    for s in soft_list.findall('softwarelist'):
        soft_list_count += 1

    print(soft_list_count, " softwares lists")

WindowManager.start(machine_count, machine_list, soft_list_count, soft_list, Config.windows_quantity)

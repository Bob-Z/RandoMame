#!/usr/bin/python3

import Arcade
import Config
import XmlGetter

Config.parse_command_line()

root = XmlGetter.get()

print("MAME version: ", root.attrib["build"])

machine_count = 0
arcade_count = 0
non_arcade_count = 0
no_input_machine = 0

for machine in root.findall('machine'):
    machine_count += 1
    machine_input = machine.find("input")
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

Arcade.start(machine_count, root)

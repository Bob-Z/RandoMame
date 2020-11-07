import random
import subprocess
import time

import Config


def start(machine_count, root):
    print("Start arcade mode")

    while True:
        rand = random.randrange(machine_count)
        machine = root[rand]

        if machine.attrib["isdevice"] == "yes":
            print("Skip device ", machine.attrib["name"])
            continue
        if machine.attrib["runnable"] == "no":
            print("Skip non runnable ", machine.attrib["name"])
            continue
        if machine.attrib["ismechanical"] == "yes":
            print("Skip mechanical ", machine.attrib["name"])
            continue

        description = machine.find("description")
        year = machine.find("year")

        full_name = "\"" + machine.attrib["name"] + "\"" + " - " + description.text + " - (" + year.text + ")"

        machine_input = machine.find('input')
        if machine_input is not None:
            if "coins" in machine_input.attrib:
                print("Run", full_name)
                time.sleep(1.5)
                run_mame(machine.attrib["name"])
            else:
                print("Skip non arcade machine ", full_name)
        else:
            print("Skip no input machine ", full_name)


def run_mame(machine_name):
    out = subprocess.Popen(
        [Config.mame_binary, "-nowindow", "-ui_active", "-skip_gameinfo", "-str", str(Config.duration), machine_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    out.communicate()

import subprocess
import time


def start(root):
    print("Start arcade mode")

    for machine in root.findall('machine'):

        description = machine.find("description")
        year = machine.find("year")

        full_name = "\"" + machine.attrib["name"] + "\"" + " - " + description.text + " - (" + year.text + ")"

        machine_input = machine.find('input')
        if machine_input is not None:
            if "coins" in machine_input.attrib:
                print("Run", full_name)
                run_mame(machine.attrib["name"])
                time.sleep(1.5)
            else:
                print("Skip non arcade machine ", full_name)
        else:
            print("Skip no input machine ", full_name)


def run_mame(machine_name):
    out = subprocess.Popen(['/media/4To/emu/mame/mame/mame64', machine_name],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)

    out.communicate()
